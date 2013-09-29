import sys

from StringIO import StringIO

from fabric.api import env, run, cd, settings, prefix, task, local, prompt, put, sudo
from fabric.contrib.console import confirm
from fabric.colors import green, red
from fabric.contrib import files
import fabtools
from fabtools.utils import run_as_root


env.virtual_env = "codemood"
env.project_user = "codemood"
env.git_repo = "git@github.com:mindinpanic/codingmood.git"
env.git_repo_name = "codemood"
env.project_name = "codemood"
env.home_dir = "/home/codemood"
env.project_root = '%(home_dir)s/src/' % env
env.project_dir = '%s%s' % (env.project_root, env.git_repo_name)
env.static_dir = '%s/%s/assets/' % (env.project_dir, env.project_name)
env.project_logs = "%slogs" % env.project_root
env.config_templates = "%s/config/" % env.project_dir
env.virtualenv_dir = "/root/.virtualenvs"
env.nginx_sites_available_dir = "/etc/nginx/sites-available/"
env.nginx_sites_available = "/etc/nginx/sites-available/codemood-site.conf"
env.nginx_sites_enabled = "/etc/nginx/sites-enabled/codemood-site.conf"
env.nginx_sites_enabled_dir = "/etc/nginx/sites-enabled/"
env.python_path = "%(virtualenv_dir)s/%(virtual_env)s/lib/python2.7/site-packages/" % env
env.python_bin = "%(virtualenv_dir)s/%(virtual_env)s/bin/python" % env
env.db_user = "postgres"
env.use_ssh_config = True
env.verbose = True



@task()
def production():
    env.hosts = ['192.241.252.102',]
    env.user = 'root'
    env.settings_module_name = "production"


def info(msg):
    if env.verbose:
        print(green(msg))


def _workon():
    workon_command = [
        "source /usr/local/bin/virtualenvwrapper.sh",
        "workon {virtual_env}".format(virtual_env=env.virtual_env),
        "export DJANGO_SETTINGS_MODULE=codemood.settings.%(settings_module_name)s" % env
    ]
    return prefix(" && ".join(workon_command))


def _compiled_conf_file(filename):
    with cd(env.config_templates):
        return run("cat %s" % filename, quiet=True) % env


@task(alias="pull")
def git_pull(remote="origin", branch="master"):
    with cd(env.project_dir):
        run('git pull {0} {1}'.format(remote, branch))


@task(alias="pip")
def pip_install():
    with settings(cd(env.project_dir), _workon()):
        run('pip install -r requirements.txt')


@task
def syncdb():
    with settings(cd(env.project_dir), _workon()):
        run('python manage.py syncdb')


def migrate():
    with settings(cd(env.project_dir), _workon()):
        run('python manage.py migrate')


def restart_supervisord():
    with _workon():
        if files.exists("/tmp/supervisord.pid"):
            run("cat /tmp/supervisord.pid | xargs kill")
        run("supervisord -c /etc/supervisord.conf ")


@task(alias="static")
def collectstatic():
    with settings(cd(env.project_dir), _workon()):
        run('python manage.py collectstatic --noinput')


def redis_service(command):
    sudo("service redis-server %s" % command, pty=False)


@task
def restart():
    redis_service("restart")
    with _workon():
        setup_nginx()
        setup_supervisor()
        run("supervisorctl restart codemood_gunicorn")
        run("supervisorctl restart codemood_celery")
    restart_supervisord()


@task
def start():
    redis_service("start")
    with _workon():
        run("supervisorctl start codemood_gunicorn")
        run("supervisorctl start codemood_celery")


@task
def stop():
    redis_service("stop")
    with _workon():
        run("supervisorctl stop codemood_gunicorn")
        run("supervisorctl stop codemood_celery")


@task(alias="run")
def run_command(command):
    with settings(cd(env.project_dir), _workon()):
        run('python manage.py %s' % command)


@task()
def setup_user(with_key):
    if not fabtools.user.exists(env.project_user):
        fabtools.user.create(env.project_user)
        if not fabtools.files.is_file('/home/{user}/.ssh/authorized_keys'.format(user=env.project_user)):
            run('mkdir -p /home/{user}/.ssh/'.format(user=env.project_user))
            run('cp /root/.ssh/authorized_keys /home/{user}/.ssh/'.format(user=env.project_user))
            run('chown {user}:{user} /home/{user}/.ssh/ -R'.format(user=env.project_user))


@task()
def setup_environment():
    fabtools.deb.update_index()

    fabtools.require.deb.packages([
        'git', 'libexpat1-dev', 'gettext libz-dev',
        'libssl-dev', 'build-essential',
        'python', 'python-dev', 'python-pip',
        'nginx', 'postgresql-9.1', 'postgresql-server-dev-9.1', 'libxml2-dev', 'libxslt-dev',
        "build-essential", "libxslt1-dev", "libcurl4-openssl-dev",
        "openssl",
        "libreadline6", "libreadline6-dev", "zlib1g", "zlib1g-dev", "libssl-dev", "libyaml-dev",
        "libsqlite3-dev", "sqlite3", "libxml2-dev", "libxslt-dev", "libpq-dev",
        "autoconf", "libc6-dev", "ncurses-dev", "automake", "libtool", "bison", "subversion",
        "gawk", "libgdbm-dev", "libffi-dev", "redis-server"
    ])

    fabtools.require.deb.nopackages([
        'rubygems',
        'rubygems1.8',
        'ruby1.8',
        'ruby1.8-dev',
    ])

    # fabtools.python.install('virtualenv', use_sudo=True)
    # fabtools.python.install('virtualenvwrapper', use_sudo=True)

    if not files.contains("~/.bashrc", "export WORKON_HOME={virtualenv_dir}".format(
            virtualenv_dir=env.virtualenv_dir)):
        files.append("~/.bashrc", "export WORKON_HOME={virtualenv_dir}".format(
            virtualenv_dir=env.virtualenv_dir))
    if not files.contains("~/.bashrc", "source /usr/local/bin/virtualenvwrapper.sh"):
        files.append("~/.bashrc", "source /usr/local/bin/virtualenvwrapper.sh")

    if not files.exists(env.virtualenv_dir):
        run("mkdir -p {virtualenv_dir}".format(virtualenv_dir=env.virtualenv_dir))

    with prefix("WORKON_HOME={virtualenv_dir}".format(virtualenv_dir=env.virtualenv_dir)):
        with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
            existent_virtual_envs = run("lsvirtualenv")
            if not env.virtual_env in existent_virtual_envs:
                run("mkvirtualenv {virtual_env}".format(virtual_env=env.virtual_env))

    if not files.exists(env.project_root):
        run("mkdir -p {project_root}".format(project_root=env.project_root))

    if not files.exists(env.project_logs):
        run("mkdir -p {project_logs}".format(project_logs=env.project_logs))


@task()
def setup_supervisor():
    with cd(env.config_templates):
        supervisord_conf = run("cat supervisord.conf", quiet=True)
        supervisord_conf_compiled = supervisord_conf % env
        put(StringIO(supervisord_conf_compiled), "/etc/supervisord.conf")
    restart_supervisord()


@task()
def setup_nginx():
    with cd(env.config_templates):
        put(StringIO(_compiled_conf_file("nginx.conf")), env.nginx_sites_available)

        if not files.exists(env.nginx_sites_enabled):
            run("ln -s {0} {1}".format(env.nginx_sites_available, env.nginx_sites_enabled))

        fabtools.require.service.restarted("nginx")


@task()
def setup_project():
    if not files.exists(env.project_dir):
        fabtools.git.clone(env.git_repo, path=env.project_dir)
    else:
        git_pull()

    with _workon():
        fabtools.python.install("mercurial")

    pip_install()

    # with settings(cd(env.project_dir), _workon()):
    #     if not files.exists('common/settings/production.py'):
    #         run("cp common/settings/production.py.example gift_exchange/settings/production.py")


@task()
def setup_db():
    fabtools.require.postgres.server()

    if not files.exists("/etc/locale.gen"):
        run("ln -s /etc/locale.alias /etc/locale.gen")

    fabtools.require.postgres.user(env.db_user, env.db_password)
    fabtools.require.postgres.database(env.virtual_env, env.db_user)


@task()
def git(command):
    with cd(env.project_dir):
        run("git {0}".format(command))


@task
def deploy():
    git_pull()
    pip_install()
    syncdb()
    migrate()
    collectstatic()
    restart()


@task()
def setup(with_key=False):
    setup_user(with_key)
    setup_environment()
    # should be before supervisor and nginx setuping
    setup_project()
    setup_supervisor()
    setup_nginx()
    setup_db()
    deploy()

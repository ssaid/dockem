#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
dockem.main
-----------------

Main entry point for the `dockem` command.
"""
from ConfigParser import ConfigParser, NoOptionError
import logging
import os
import getpass
from subprocess import Popen

logger = logging.getLogger(__name__)

def create_config_file():
    name = os.path.basename(os.getcwd())
    username = getpass.getuser()
    ## lets create that config file for next time...
    cfgfile = open("config.ini",'w')

    # add the settings to the structure of the file, and lets write it out...
    Config = ConfigParser()
    Config.add_section('Container')
    Config.set('Container', 'name', name)
    Config.set('Container', 'host', name)
    Config.set('Container', 'image', username + "/odoo_ubuntu:12.04")
    Config.set('Container', 'volumes', 'Vol1, Vol2, Vol3')
    Config.set('Container', 'remove', True)
    Config.set('Container', 'data_container', name + 'db')
    Config.set('Container', 'ports', 'Port1, Port2')
    Config.set('Container', 'env', 'DB_ENV_DB_USER:odoodev, DB_ENV_DB_PASS:pass')

    Config.add_section('Vol1')
    Config.set('Vol1', 'localdir', '$PWD/build')
    Config.set('Vol1', 'containerdir', '/opt/buildout')
    Config.add_section('Vol2')
    Config.set('Vol2', 'localdir', '$HOME/.buildout/odoo7')
    Config.set('Vol2', 'containerdir', '/opt/buildout/parts/odoo')
    Config.add_section('Vol3')
    Config.set('Vol3', 'localdir', '$HOME/.buildout/dlcache')
    Config.set('Vol3', 'containerdir', '/opt/buildout/dlcache')

    Config.add_section('Port1')
    Config.set('Port1', 'localport', '8069')
    Config.set('Port1', 'containerport', '8069')
    Config.add_section('Port2')
    Config.set('Port2', 'localport', '5432')
    Config.set('Port2', 'containerport', '5432')

    Config.write(cfgfile)
    cfgfile.close()


def _read_config_file(file):
    config = ConfigParser()
    config.read(file)
    return config

def execute_container():
    # Tomamos los datos del config.ini
    config = _read_config_file('config.ini')

    rm = True
    data_container = ''
    ports = []
    volumes = []
    host = ''

    section = "Container"

    if not config.has_section(section):
        logger.critical("No existe seccion %s en config.ini" % section)
        exit(-1)

    # Obtenemos los datos de esta seccion
    try:
        container_name = config.get(section, "name")
        image_name = config.get(section, "image")
    except NoOptionError, e:
        logger.exception("Error en config.ini [%s]" % e)
        exit(-1)

    if config.has_option(section, "remove"):
        rm = config.getboolean(section, "remove")
    else:
        logger.warning("No se setea la opcion remove en config.ini. Por defecto es %s" % rm)

    if config.has_option(section, "data_container"):
        data_container = config.get(section, "data_container")
    else:
        logger.warning("No hay opcion data_container")

    if config.has_option(section, "host"):
        host = config.get(section, "host")
    else:
        logger.warning("No se setea la opcion host en config.ini." % rm)

    # Environment
    envs = []
    if config.has_option(section, "env"):
        envvars = config.get(section, "env")

        envvars = envvars.replace(' ', '').split(',')
        for var in envvars:
            k, v = var.split(':')
            envs.append("%s=%s" % (k, v))

    # Volumenes
    try:
        vols = config.get(section, "volumes")

        if vols:
            vols = vols.replace(' ', '').split(',')

        for sec in vols:
            if not config.has_section(sec):
                logger.critical("No existe seccion %s en config.ini" % sec)
                exit(-1)

            localdir = config.get(sec, "localdir")
            containerdir = config.get(sec, "containerdir")
            volumes.append("%s:%s" % (localdir, containerdir))

    except NoOptionError, e:
        logger.warning("No hay definicion de volumenes [%s]" % e)

    # Puertos
    try:
        pts = config.get(section, "ports")

        if pts:
            pts = pts.replace(' ', '').split(',')

        for sec in pts:
            if not config.has_section(sec):
                logger.critical("No existe seccion %s en config.ini" % sec)
                exit(-1)

            localport = config.get(sec, "localport")
            containerport = config.get(sec, "containerport")
            ports.append("%s:%s" % (localport, containerport))

    except NoOptionError, e:
        logger.warning("No hay definicion de puertos [%s]" % e)

    logger.info("Creando container %s a partir de imagen => %s" % (container_name, image_name))
    cmd_t = ["docker run", "-t", "-i"]

    if rm:
        cmd_t.append("--rm")

    if host:
        cmd_t.append("-h")
        cmd_t.append(host)

    if ports:
        logger.info("Puertos definidos: ")
    for p in ports:
        cmd_t.append("-p")
        cmd_t.append(p)
        logger.info(p)

    if volumes:
        logger.info("Volumenes definidos: ")
    for v in volumes:
        cmd_t.append("-v")
        cmd_t.append(v)
        logger.info(v)

    if envs:
        logger.info("Variables de Entorno: ")
    for e in envs:
        cmd_t.append("-e")
        cmd_t.append(e)
        logger.info(e)

    if data_container:
        # TODO: Chequear que existe el container de datos
        #_check_container_exists()
        cmd_t.append("--volumes-from")
        cmd_t.append(data_container)
        logger.info("Container de datos definido: %s" % data_container)

    if container_name:
        cmd_t.append("--name")
        cmd_t.append(container_name)
    else:
        logger.warning("No hay un nombre definido para el container")

    cmd_t.append(image_name)

#     cmd_t = ["docker run", "-t", "-i", "--rm", "-p", "8099:8069",
#           "-v", "$PWD/build:/opt/buildout",
#           "-v", "$HOME/.buildout/odoo7:/opt/buildout/parts/odoo",
#           "--volumes-from", "testdb",
#           "--name", "odootest", "skennedy/odoo_ubuntu:12.04"]

    cmd = ' '.join(cmd_t)
    logger.info("Comando a ejecutar: %s" % cmd)
    p = Popen(cmd, shell=True)
    p.communicate()

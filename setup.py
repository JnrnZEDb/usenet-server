#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Copyright (C) 2016 Maskaliova, Schroer, Zelnick.
# 
# All rights reserved. No part of this publication may be reproduced,
# distributed, or transmitted in any form or by any means, including
# photocopying, recording, or other electronic or mechanical methods,
# without the prior written permission of the publisher, except in the
# case of brief quotations embodied in critical reviews and certain other
# noncommercial uses permitted by copyright law.

from sys import exit
from setuptools import setup

if( __name__ != '__main__' ):
        exit( -1 )
else:
        config = {
            'name' : 'usenet_server',
            'description' : 'usenet server implementation',
            'url' : '',
            'download_url' : '',
            'author_email' :
            'rzelnick@cs.stonybrook.edu,gene.schroer@stonybrook.edu',
            'version' : '0.7.1',
            'install_requires' : [ 'nose', 'sphinx' ],
            'packages' : [ 'core' ],
            'scripts' : [ 'bin/server.py' ]
        }

        setup( **config )

# vim: number ts=4 sw=4 expandtab tw=76

===============================
piambientlight
===============================


.. image:: https://img.shields.io/pypi/v/piambientlight.svg
        :target: https://pypi.python.org/pypi/piambientlight

.. image:: https://img.shields.io/travis/coleslaw481/piambientlight.svg
        :target: https://travis-ci.org/coleslaw481/piambientlight

.. image:: https://readthedocs.org/projects/piambientlight/badge/?version=latest
        :target: https://piambientlight.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/coleslaw481/piambientlight/shield.svg
     :target: https://pyup.io/repos/github/coleslaw481/piambientlight/
     :alt: Updates


Ambient light driver for Rasberry PI using PI Camera

The goal of this project is to develop a completely passive ambient LED lighting system using a Rasberry Pi with an attached Pi camera. Not totally sure this will work, but figured it would be a fun project to attempt. 

.. image:: https://github.com/coleslaw481/piambientlight/blob/master/images/overview.png

The figure above summarizes the idea. Basically a Rasberry Pi with a Pi camera is pointed at the TV. This software then analyzes the image from the Pi camera extracting pixel color values for pixels in the green boxes in the figure above. The pixel values are then converted to color values on a LED light strip. 

* Free software: GNU General Public License v3
* Documentation: https://piambientlight.readthedocs.io.


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


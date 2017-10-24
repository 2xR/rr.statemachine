===============
rr.statemachine
===============

This library defines classes for discrete state machines (the ``StateMachine`` base class), finite state machines (``FiniteStateMachine``) and Markov chains (``MarkovChain``).

Handler functions are invoked when entering/leaving a state (``on_enter()`` and ``on_exit()``), and it the middle of a transition when the machine's state is actually undefined for a brief period (``on_transition()``).

See ``src/rr/statemachine/__init__.py`` for example applications of FSAs and Markov chains.


Compatibility
=============

Developed and tested in Python 3.6+. The code may or may not work under earlier versions of Python 3 (perhaps back to 3.3).


Installation
============

From the github repo:

.. code-block:: bash

    pip install git+https://github.com/2xR/rr.statemachine.git


License
=======

This library is released as open source under the MIT License.

Copyright (c) 2017 Rui Rei

2. Releasing into DLS python 3
==============================

Date: 2023-01-20

Status
------

Accepted

Context
-------

As the skeleton has evolved, it has diverged from the architecture that the build 
server expects and the packages that it provides. In light of this, there is a need 
to provide a version of the skeleton that is accepted by the current internal release 
process.

Decision
--------

We will provide a branch of the skeleton that adopts the necessary files to be
build server compatible. This serves as a stop gap for internally released tools
until the build server is removed, at which point we will upgrade to the latest 
skeleton version.

Consequences
------------

* We will be able to adopt the skeletons archtecture and features, yet still 
  release the tools internally.
* We will not be able to adopt future improvements to the skeleton.

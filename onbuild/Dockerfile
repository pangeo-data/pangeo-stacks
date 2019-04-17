ARG BASE_IMAGE_SPEC
FROM $BASE_IMAGE_SPEC

USER root
COPY r2d_overlay.py /usr/local/bin/r2d_overlay.py

ONBUILD COPY --chown=1000:1000 . ${REPO_DIR}
# We copy contents of *child* image to a subdirectory temporarily
# This helps us apply customizations that were only from the
# child, and re-do the packages of the parent.
ONBUILD COPY --chown=1000:1000 . ${REPO_DIR}/.onbuild-child
ONBUILD RUN /usr/local/bin/r2d_overlay.py build
ONBUILD RUN rm -rf ${REPO_DIR}/.onbuild-child

ONBUILD USER ${NB_USER}
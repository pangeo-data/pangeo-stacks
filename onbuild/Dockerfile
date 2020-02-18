ARG BASE_IMAGE_SPEC
FROM $BASE_IMAGE_SPEC

USER root
COPY r2d_overlay.py /usr/local/bin/r2d_overlay.py

# We aren't using --chown here since a bunch of binders
# don't run new enough Docker for it.
ONBUILD COPY . ${REPO_DIR}
# We copy contents of *child* image to a subdirectory temporarily
# This helps us apply customizations that were only from the
# child, and re-do the packages of the parent.
ONBUILD COPY . ${REPO_DIR}/.onbuild-child
ONBUILD RUN chown -R 1000:1000 ${REPO_DIR}
ONBUILD RUN /usr/local/bin/r2d_overlay.py build
ONBUILD RUN rm -rf ${REPO_DIR}/.onbuild-child

ONBUILD USER ${NB_USER}

ENTRYPOINT ["/usr/local/bin/r2d_overlay.py", "start"]

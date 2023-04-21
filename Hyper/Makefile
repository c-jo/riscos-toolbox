# Makefile for !Hyper

COMPONENT     = Hyper
TARGET        = !RunImage

OBJS          = button commands draw file handler hcl main menus print utils view
CINCLUDES     = -Itbox:,C:
LIBS          = ${EVENTLIB} ${TBOXLIB} ${WIMPLIB} ${RENDERLIB}

INSTDIR      ?= <Install$Dir>
INSTAPP_FILES = !Boot !Help !Run ${TARGET} !Sprites !Sprites11 !Sprites22 Messages Res

include CApp

C_WARNINGS = -fa

clean_all:: clean
	${WIPE} ${INSTAPP} ${WFLAGS}

# Dynamic dependencies:

/*
 * Copyright Commissariat à l'énergie atomique et aux énergies alternatives (CEA).
 * All rights reserved. Access to and use of this software is restricted to authorized users only.
 * Authorized users may only use the software in accordance with the terms of the user license
 * granted to them
 */
/*
 * File:   libpmcccommon.h
 * Author: gchagnet
 *
 * Created on 20 february 2013, 16:26
 */

#ifndef LIBPMCCCOMMON_H
#define LIBPMCCCOMMON_H

#include <QtCore/QtGlobal>

#ifdef _WIN32
#ifdef LIB_EXPORT
#define LIBCOMMON_EXPORT Q_DECL_EXPORT
#else
#define LIBCOMMON_EXPORT Q_DECL_IMPORT
#endif
#else
#define LIBCOMMON_EXPORT
#endif

#endif /* LIBPMCCCOMMON_H */

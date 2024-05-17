/*
 * Copyright Commissariat à l'énergie atomique et aux énergies alternatives (CEA).
 * All rights reserved. Access to and use of this software is restricted to authorized users only.
 * Authorized users may only use the software in accordance with the terms of the user license
 * granted to them
 */
#ifndef PMCCMANAGER_H
#define PMCCMANAGER_H

#include <PMCCErrorCode.h>
#include <libpmcccommon.h>

#include <QtCore/QMap>
#include <QtCore/QSharedPointer>
#include <QtCore/QVariant>

/// Forward declaration
class Pmcc5;

/**
 * @brief The PmccManager class is the high-level API of the PMCC algorithm. The user customize the
 * algorithm execution by setting options and arguments.
 *
 * Example:
 *
 * // Declare the pmcc manager
 * PmccManager pmcc;
 *
 *  // Add options
 *  // Family detection, a cdf file is required.
 *  pmcc.addOption("-f", "path_to_cdf_file.cdf");
 *
 *  // Add arguments
 *  pmcc.addArgument("st", "2005/12/11 06:00:00.000");
 *  pmcc.addArgument("et", "2005/12/11 07:00:00.000");
 *  pmcc.addArgument("sta", "TEST");
 *  pmcc.addArgument("par", "pmcc.par");
 *  pmcc.addArgument("par", "pmcc_specific.par");
 *
 *  // Add optional arguments
 *  pmcc.addArgument("bul" , "bulletin.txt");
 *
 *  // Execute PMCC algorithm
 *  PMCC_ERROR errorCode = pmcc.execute();
 *
 *  // Retrieve results
 *  QStringList families = pmcc.getFamilies();
 *  QStringList pixels = pmcc.getPixels();
 */
class LIBCOMMON_EXPORT PmccManager {
public:
    /**
     * @brief The class constructor
     */
    explicit PmccManager();

    /**
     * The class destructor
     */
    virtual ~PmccManager();

    /**
     * @brief Add an option to the pmcc algorithm.
     * @param option The option to add.
     * @param value The value associated to the option (not required).
     *
     * The available options are:
     * - -d or --detec : Enables the detection mode of the PMCC algorithm.
     * - -f or --families : Enables the family mode of the PMCC algorithm. This option requires a
     * file path to the PMCC detection.
     * - -V or --version : Displays the version of the PMCC algorithm.
     * - -v or --verbose : Enables the verbose mode.
     * - -h or --help : Displays the PMCC help.
     */
    void addOption(const QString &option, const QVariant &value = QVariant());

    /**
     * @brief Add options to the pmcc algorithm.
     * @param parameters The options to add.
     *
     * The available options are:
     * - -d or --detec : Enables the detection mode of the PMCC algorithm.
     * - -f or --families : Enables the family mode of the PMCC algorithm. This option requires a
     * file path to the PMCC detection.
     * - -V or --version : Displays the version of the PMCC algorithm.
     * - -v or --verbose : Enables the verbose mode.
     * - -h or --help : Displays the PMCC help.
     */
    void addOptions(const QMap<QString, QVariant> &parameters);

    /**
     * @brief Add an argument to the pmcc algorithm.
     * @param argument The argument to add.
     * @param value The value associated to the argument.
     *
     * The required arguments are:
     * - st : starting datetime in Unix or YYYY/MM/DD-HH:MM:SS.ZZZ format.
     * - et : ending datetime in Unix or YYYY/MM/DD-HH:MM:SS.ZZZ format.
     * - sta : name of the array station.
     * - par : configuration file, usually called pmcc.par.
     *
     * The optional arguments are:
     * - bul : bulletin file name. The file will be saved in the directory out-OutputDir provided in
     * the configuration file.
     * - FileType : type of the data files. (CSS, Seed, Fonyx).
     * - FlagScanDir : flag to enable or not the subdirectory scanning.
     * - FlagSDSTree : flag to enable or not the SDS Tree scanning for the SEED data.
     */
    void addArgument(const QString &argument, const QVariant &value);

    /**
     * @brief Add arguments to the pmcc algorithm.
     * @param parameters The arguments to add.
     *
     * The required arguments are:
     * - st : starting datetime in Unix or YYYY/MM/DD-HH:MM:SS.ZZZ format.
     * - et : ending datetime in Unix or YYYY/MM/DD-HH:MM:SS.ZZZ format.
     * - sta : name of the array station.
     * - par : configuration file, usually called pmcc.par.
     *
     * The optional arguments are:
     * - bul : bulletin file name. The file will be saved in the directory out-OutputDir provided in
     * the configuration file.
     * - FileType : type of the data files. (CSS, Seed, Fonyx).
     * - FlagScanDir : flag to enable or not the subdirectory scanning.
     * - FlagSDSTree : flag to enable or not the SDS Tree scanning for the SEED data.
     */

    void addArguments(const QMap<QString, QVariant> &parameters);

    /**
     * @brief Execute the PMCC algorithm using the added options and arguments.
     * @return An PMCC_ERROR.
     */
    PMCC_ERROR execute();

    /**
     * @brief Reset the parameters set of the PMCC algorithm.
     */
    void reset();

    /**
     * @brief Get the filepath of the cdf generated file.
     * @return The CDF filepath.
     */
    QString getNetCDFResultFile() const;

    /**
     * @brief Get the PMCC parameters.
     * @return The list of parameters.
     */
    QMap<QString, QVariant> getParameters() const;

protected:
    /// The PMCC algorithm.
    QSharedPointer<Pmcc5> m_PMCC;

    /// The PMCC parameters.
    QMap<QString, QVariant> m_Parameters;
};

#endif // PMCCMANAGER_H

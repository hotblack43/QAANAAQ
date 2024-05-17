# How to use the PMCC library

* Install the PMCC library and header on your computer.
* Link the application with the shared `pmcc` library.
* Add the path of `PmccManager` header to the include path of the application project.
* Include `PmccManager`header.
* Configure the `pmcc` algorithm and execute it.
* Retrive the detection results.

# Example

~~~{.cpp}
   
#include <QStringList>
#include <QDebug>
#include <PmccManager.h>

int main(int argc, char *argv[]) 
{
	// Declare the pmcc manager
	PmccManager pmcc;
	 
	// Add options
	// Family detection, a cdf file is required.
	pmcc.addOption("-f", "path_to_cdf_file.cdf");
	 
	// Add arguments
	pmcc.addArgument("st", "2005/12/11 06:00:00.000");
	pmcc.addArgument("et", "2005/12/11 07:00:00.000");
	pmcc.addArgument("sta", "TEST");
	pmcc.addArgument("par", "pmcc.par");
	pmcc.addArgument("par", "pmcc_specific.par");
	
	// Add optional arguments
	pmcc.addArgument("bul" , "bulletin.txt");
	 
    // Execute PMCC algorithm
	PMCC_ERROR errorCode = pmcc.execute();
	
	// Retrieve results
	QStringList families = pmcc.getFamilies();
	QStringList pixels = pmcc.getPixels();

	// Do something with the results...
	// ...
	qDebug() << "Found families : " << families.size();
	qDebug() << "Found pixels : " << pixels.size();

	return errorCode;	 
}  
~~~

See the API documentation for more informations on `pmcc` library.
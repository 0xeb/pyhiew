//
//  Hem2hem gate usage sample
//  Call from sample1
//

#include "hem.h"

////////////////////////////////////////////////////////////

#define   HEM_SAMPLE2_VERSION_MAJOR     1
#define   HEM_SAMPLE2_VERSION_MINOR     1

////////////////////////////////////////////////////////////

int HEM_API
 HemSample2Gate( void * );

////////////////////////////////////////////////////////////

HEMINFO_TAG
  hemSample2={ sizeof( HEMINFO_TAG ), 
               sizeof( int ),
               0,                   // reserved
               HEM_SDK_VERSION_MAJOR,     HEM_SDK_VERSION_MINOR,
               HEM_SAMPLE2_VERSION_MAJOR, HEM_SAMPLE2_VERSION_MINOR,
               0,                   // hemFlag
               0,                   // reserved
               NULL,                // no Hem_EntryPojnt()  
               NULL,                // no Hem_Unload()
               HemSample2Gate,
               0,                   // reserved
               0,                   // reserved
               0,                   // reserved
               0,                   // reserved
               "Sample TWO",
               "Hiew External Module: sample 2",
               "",
               "Hem-to-hem Gate",
               "",
              };

////////////////////////////////////////////////////////////

int HEM_EXPORT
 Hem_Load( HIEWINFO_TAG *hiewInfo )
{
 HiewGate_Set( hiewInfo );
 hiewInfo->hemInfo=&hemSample2;
 return( HEM_OK );
}

////////////////////////////////////////////////////////////

int HEM_API
 HemSample2Gate( void *parm )
{
 return( HiewGate_Message( " SAMPLE NUMBER TWO ", parm ) );
}

////////////////////////////////////////////////////////////


//
// Setting new offset / calculating bytesum
// Only active for PE files with block marked in hex mode
//
//// Usage sample for functions:
//
//  HiewGate_GetData()
//  HiewGate_Menu()
//  HiewGate_Message()
//  HiewGate_GetMemory()
//  HiewGate_FreeMemory()
//  HiewGate_FileRead()
//

#include "hem.h"

#include <stdio.h>    // for sprintf()

////////////////////////////////////////////////////////////

#define   HEM_SAMPLE3_VERSION_MAJOR     1
#define   HEM_SAMPLE3_VERSION_MINOR     20

////////////////////////////////////////////////////////////

int HEM_API
 Hem_EntryPoint( HEMCALL_TAG *hemCall );

////////////////////////////////////////////////////////////

HEMINFO_TAG
  hemSample3={ sizeof( HEMINFO_TAG ), 
               sizeof( int ),
               0,                   // reserved
               HEM_SDK_VERSION_MAJOR,     HEM_SDK_VERSION_MINOR,
               HEM_SAMPLE3_VERSION_MAJOR, HEM_SAMPLE3_VERSION_MINOR,
               HEM_FLAG_MARKEDBLOCK | HEM_FLAG_PE | HEM_FLAG_HEX,
               0,                   // reserved
               Hem_EntryPoint,
               NULL,                // no Hem_Unload()
               NULL,                // no Hem2HemGate()
               0,                   // reserved
               0,                   // reserved
               0,                   // reserved
               0,                   // reserved
               "Sample THREE",
               "Hiew External Module: sample 3",
               "Sets new offset / Calculates sum",
               "Only PE files with MARKed block in HEX mode",
               ""
              };

////////////////////////////////////////////////////////////

int HEM_EXPORT
 Hem_Load( HIEWINFO_TAG *hiewInfo )
{
 HiewGate_Set( hiewInfo );
 hiewInfo->hemInfo=&hemSample3;
 return( HEM_OK );
}

////////////////////////////////////////////////////////////

int HEM_API
 Hem_EntryPoint( HEMCALL_TAG *hemCall )
{
 if( hemCall->cbSize < sizeof( HEMCALL_TAG ) ) 
   return( HEM_ERROR );
{
 HEM_BYTE         *menu[]={ "Set cursor to START of the block", 
                            "Set cursor to  END  of the block",
                            "Calculate sum of all bytes" };
 HIEWGATE_GETDATA  hiewData;
 int               rc=HiewGate_GetData( &hiewData );

 if( rc >= 0 ){
   switch( HiewGate_Menu( "", menu, sizeof(menu)/sizeof(HEM_BYTE*), 40, 1, NULL, NULL, 0, 0 ) ){
     case 1: hemCall->returnOffset=hiewData.offsetMark1; 
             hemCall->returnActionFlag |= HEM_RETURN_SETOFFSET;
             rc=101;
             break;
     case 2: hemCall->returnOffset=hiewData.offsetMark2; 
             hemCall->returnActionFlag |= HEM_RETURN_SETOFFSET; 
             rc=202;
             break;
     case 3: { HEM_BYTE  *p, line[ 80 ]; 
               HEM_UINT   i; 
               HEM_DWORD  sum=0;
               HEM_UINT   blocksize=(HEM_UINT)hiewData.sizeMark;
             if( hemCall->hemFlag & HEM_FLAG_MARKEDBLOCK && blocksize <= 1000000 ){
               p=HiewGate_GetMemory( blocksize );
               if( p == NULL )
                 HiewGate_Message( "", "Error allocating memory" );
                else{
                 if( HiewGate_FileRead( hiewData.offsetMark1, blocksize, p ) == (int)blocksize ){
                   for( i=0; i < blocksize; i++ )
                     sum+=p[ i ];
                   sprintf( line, "Sum is %.8lX/%lu", sum, sum );
                   HiewGate_Message( "", line );
                 }else
                   HiewGate_Message( "", "Error reading file" );
                 HiewGate_FreeMemory( p );
               }
             }else
               HiewGate_Message( "", "Block is too long" );
             rc=303;
             }
             break;
   }
 }
 return( rc );   // rc < 0 means error
}
}

////////////////////////////////////////////////////////////


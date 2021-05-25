//
// 1. Usage sample for functions:
//    HiewGate_GetData()
//    HiewGate_Menu()
//    HiewGate_Message()
//    HiewGate_Window()
//    HiewGate_GetString()
//    HiewGate_GetHem2HemGate()
//
// 2. Usage sample for return values controlling:
//    mode
//    offset
//
// 3. Usage sample for Fn-key press (HEM SDK 0.21)
//
// 4. Added sample for HEM SDK 0.30:
//    HiewGate_MessageWaitOpen
//    HiewGate_MessageWaitClose
//    HiewGate_IsKeyBreak
//

#include "hem.h"

#include <string.h>   // for strcpy()
#include <stdio.h>    // for sprintf()
#include <windows.h>  // for sleep()

////////////////////////////////////////////////////////////

#define   HEM_SAMPLE1_VERSION_MAJOR     1
#define   HEM_SAMPLE1_VERSION_MINOR     20

////////////////////////////////////////////////////////////

int HEM_API
 Hem_Unload( void ),
 Hem_EntryPoint( HEMCALL_TAG *hemCall );

////////////////////////////////////////////////////////////

HEMINFO_TAG
  hemSample1={ sizeof( HEMINFO_TAG ), 
               sizeof( int ),
               0,                   // reserved
               HEM_SDK_VERSION_MAJOR,     HEM_SDK_VERSION_MINOR,
               HEM_SAMPLE1_VERSION_MAJOR, HEM_SAMPLE1_VERSION_MINOR,
               HEM_FLAG_MODEMASK|HEM_FLAG_FILEMASK,
               0,                   // reserved
               Hem_EntryPoint,
               Hem_Unload,
               NULL,
               0,                   // reserved
               0,                   // reserved
               0,                   // reserved
               0,                   // reserved
               "Sample ONE",
               "Hiew External Module: sample 1",
               "******************************************",
               "This HEM is active for any files and disks",
               "******************************************"
              };

HEM_BYTE
  hiewSdkVerMajor, hiewSdkVerMinor,
  hiewVerMajor,    hiewVerMinor;

////////////////////////////////////////////////////////////

int HEM_EXPORT
 Hem_Load( HIEWINFO_TAG *hiewInfo )
{
 hiewVerMajor=hiewInfo->hiewVerMajor;
 hiewVerMinor=hiewInfo->hiewVerMinor;
 hiewSdkVerMajor=hiewInfo->sdkVerMajor;
 hiewSdkVerMinor=hiewInfo->sdkVerMinor;
 HiewGate_Set( hiewInfo );
 hiewInfo->hemInfo=&hemSample1;
 return( HEM_OK );
}

////////////////////////////////////////////////////////////

int HEM_API
 Hem_Unload()
{
 return( HEM_OK );
}

////////////////////////////////////////////////////////////

int HEM_API
 Hem_EntryPoint( HEMCALL_TAG *hemCall )
{
 if( hemCall->cbSize < sizeof( HEMCALL_TAG ) ) 
   return( HEM_ERROR );

// --- HEM code starts here
{
#define   INFO_LINES                   7
#define   INFO_LINE_MAXLEN             60
#define   LINEBYE_MAXLEN               40
#define   MENU_COUNT                  ( sizeof(menu)/sizeof(HEM_BYTE*) )
#define   MENU_WIDTH                   30

 HEM_FNKEYS 
//          "123456789ABC|F1____F2____F3____F4____F5____F6____F7____F8____F9____F10___F11___F12___"
  fnKeys={  "010000000000|      Active      Pasive                                                ",   // main Fn
            "",   // no Alt-Fn
            "",   // no Ctrl-Fn
            "000000000100|                                                      Exit              " }; // ShiftFn
 HEM_BYTE
   info[ INFO_LINES ][ INFO_LINE_MAXLEN ],
   *pInfo[ INFO_LINES ],
   *menu[]={ "Hiew version",
             "HEMCALL_TAG view",
             "Name input", 
             "Call Sample2",
             "Set return: mode & offset",
             "Message wait test",
            },
   name[ LINEBYE_MAXLEN ],    // including terminating zero
   lineBye[ LINEBYE_MAXLEN*2 ];
 int
  i,
  item,
  rc;
 HEM_UINT
  pressedFnKey;
 HIEWGATE_GETDATA
  hiewData;
 HIEWGATE_GETHEM2HEMGATE
  hemGate;                     

// get hiew data
 rc=HiewGate_GetData( &hiewData );
 if( rc < 0 )
   return( rc );

 strcpy( lineBye, "Bye!" );
 HiewGate_GetHem2HemGate( &hemGate, "SAMPLE TWO" );
 item=1; // first menu item 
 while( (item=HiewGate_Menu( " Menu ", menu, MENU_COUNT, MENU_WIDTH, item, &fnKeys, &pressedFnKey, 0, 0 )) != HEM_INPUT_ESC ){
   if( pressedFnKey ){
     if( pressedFnKey == HEM_FNKEY_F2 )       HiewGate_Message( "", "F2 is active and pressed" );
     if( pressedFnKey == HEM_FNKEY_F4 )       HiewGate_Message( "", "F4 is NEVER press" );
     if( pressedFnKey == HEM_FNKEY_SHIFTF10 ) return( HEM_OK );
   }else
     if( item == 1 ){   // "Hiew version",
       sprintf( &info[0][0], "Hiew %d.%.2d, SDK %d.%.2d", hiewVerMajor, hiewVerMinor, hiewSdkVerMajor, hiewSdkVerMinor );
       HiewGate_Message( " HEM NUMBER ONE ", info[0] ); 
     }else
       if( item == 2 ){   // "HEMCALL_TAG view",
         i=0;
         sprintf( pInfo[i++]=&info[i][0], "HemFlag:    %.8lX", hemCall->hemFlag );
         sprintf( pInfo[i++]=&info[i][0], "Mode:       %s", 
                  ( hemCall->hemFlag & HEM_FLAG_TEXT ) ? "Text" :
                  ( hemCall->hemFlag & HEM_FLAG_HEX  ) ? "Hex"  :
                  ( hemCall->hemFlag & HEM_FLAG_CODE ) ? "Code" : "???" );
         sprintf( pInfo[i++]=&info[i][0], "Filename:   %-40.40s", hiewData.filename );
         sprintf( pInfo[i++]=&info[i][0], "Filelength: %I64d bytes", hiewData.filelength );
         sprintf( pInfo[i++]=&info[i][0], "Offset:     %.16I64X", hiewData.offsetCurrent );
         if( hemCall->hemFlag & HEM_FLAG_MARKEDBLOCK )
           sprintf( pInfo[i++]=&info[i][0], "Block:      %.16I64X-%.16I64X", hiewData.offsetMark1, hiewData.offsetMark2 );
         sprintf( pInfo[i++]=&info[i][0], "Sample2Gate:%.8lX", hemGate.Hem2HemGate );
         HiewGate_Window( " Sample 1 ", pInfo, i, 0, NULL, NULL );
       }else
         if( item == 3 ){   // "Name input", 
           strcpy( name, "...Type name here..." );
           if( HiewGate_GetString( " Name Input ", name, LINEBYE_MAXLEN ) == HEM_INPUT_CR )
             sprintf( lineBye, "Bye, %s!", name );
            else
             strcpy( lineBye, "Bye!" );
         }else
           if( item == 4 ){   // "Call Sample2",
             if( hemGate.Hem2HemGate )
               hemGate.Hem2HemGate( "Hello from sample ONE!" );  
              else
               HiewGate_Message( "", "Hem2HemGate() not found" );
           }else
             if( item == 5 ){   // "Set return: mode & offset",
               hemCall->returnActionFlag |= HEM_RETURN_SETMODE;
               hemCall->returnMode=HEM_RETURN_MODE_HEX;
               hemCall->returnActionFlag |= HEM_RETURN_SETOFFSET;
               hemCall->returnOffset=0;
               break;           // 'while' break and return to host
             }else
               if( item == 6 ){   // "Message wait test"; SDK version 0.30
                 if( HiewGate_MessageWaitOpen( "Dummy loop, press ESC for break..." ) == HEM_OK ){
                   while( HiewGate_IsKeyBreak() != HEM_KEYBREAK )
                     Sleep( 250 );  // sleep 1/4 sec
                   HiewGate_MessageWaitClose();
                 }else
                   HiewGate_Message( "", "The function 'MessageWait()' is not supported" );
               }else
                 return( item );     
 }
 HiewGate_Message( " Sample 1 ", lineBye );
}
// --- HEM code ends here

 return( HEM_OK );
}

////////////////////////////////////////////////////////////


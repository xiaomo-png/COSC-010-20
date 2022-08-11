'''
################## Table Of Contents: 6 steps to follow         ##################
################## STEP_1. Login User Account                   ##################
################## STEP_2. Get Info. Of User Account            ##################
################## STEP_3. Playlist Operation                   ##################
################## STEP_4. DAILY PLAYLIST RECOMMENDATIONS       ##################
################## STEP_5. GET RECOMMENDATIONS ABOUT ARTIST     ##################
################## STEP_6. GET SONGS OF THE RECOMMENDED ARTISTS ##################
'''

import getpass
import sys
# STEP_1_FUNCTION #
from Supporting_Func import get_cookie_login_by_phoneAndPassword
# STEP_2_FUNCTION #
from Supporting_Func import get_user_account
# STEP_3_FUNCTION #
from Supporting_Func import create_playlist as create
from Supporting_Func import delete_playlist as delete
from Supporting_Func import get_playlist_by_uid
# STEP_4_FUNCTION #
from Supporting_Func import daily_recommendation
from Supporting_Func import get_recommendation
from Supporting_Func import get_songs_from_artists

import Supporting_Func

if __name__ == "__main__":
    print("################################################################################")
    print("################################ [STEP_1] Login User Account ###################")
    print("################################################################################")
    print("--------------------------------")
    print("\n---LOGIN BY PHONE & PASSWORD---\n")
    phone = input("please enter your phone number:")
    print("please enter your password:")
    password = getpass.getpass(stream=sys.stderr, prompt='Ascending Order:\n')
    try:
        userInfo, identify_cookie = get_cookie_login_by_phoneAndPassword(phone, password)
        cookie = userInfo['cookie']
        for items in cookie.split(";"):
            if items != "":
                key, value = items.split("=")
                if key == "MUSIC_U":
                    identify_cookie[key] = value
        print("\n-------------------------------\n")
    except:
        print("\n--------------  INCORRECT INFOR OR STATUS CODE == '460' !!! -----------------\n")
        exit()
    print("################################################################################")
    print("################################ [STEP_2] Get Info. Of User Account ############")
    print("################################################################################")
    Boolean_account = input("1.GET INFO ABOUT USER ACCOUNT... True/False(e.g. False)\n")
    accountInfo = get_user_account(identify_cookie)['account']  # or userInfo['account']
    if Boolean_account == "True":
        if accountInfo is not None:
            for key, value in accountInfo.items():
                print("{:<16}\t|\t{:<30}".format(key, value))
        else:
            print("Failed to get account")

    print()
    print("################################################################################")
    print("################################ [STEP_3] Playlist Operation ###################")
    print("################################################################################")
    operation_name = "True"
    while operation_name != "skip":
        print("#################################################################################################")
        operation_name = input("please write down a kind of operation to execute: (e.g. show or create or delete or skip)\n")
        print("##################################################################################################")
        ################################ [3.1] show ##########################
        if operation_name == 'show':
            print("\n---------------[STEP_3.1] SHOW ALL PLAYLIST------------------")
            playlist_info = get_playlist_by_uid(accountInfo['id'])['playlist']
            playlist_IDs = []
            print("{:<25}{:<16}{:<40}{:<16}{:<16}".format("PLAYLIST NAME", "ID", "TAGS", "CREATE TIME", "UPDATE TIME"))
            for items in playlist_info:
                print("{:<25}{:<16}{:<40}{:<16}{:<16}".format(items['name'], items['id'], ' '.join(
                    items['creator']['expertTags'] if items['creator']['expertTags'] else ['']), items['createTime'], items['updateTime']))
                playlist_IDs.append(items['id'])
        ################################ [3.2] create ##########################
        elif operation_name == 'create':
            print("\n------------------[STEP_3.2] CREATE PLAYLIST------------------\n")
            playlist_info = create(cookie=identify_cookie, name="create playlist", type="VIDEO", privacy=10)['playlist']
            print("THE NEW PLAYLIST...name:" + playlist_info['name'], "...id:", playlist_info['id'], "...createTime", playlist_info['createTime'])
            playlist_id = playlist_info['id']
        ################################ [3.3] delete ##########################
        elif operation_name == 'delete':
            print("\n------------------[STEP_3.3] DELETE PLAYLIST------------------\n")
            playlist_id = input("which playlist would you like to delete:")
            playlist_info = delete(cookie=identify_cookie, id=playlist_id)
            print(playlist_info)
        print("---------- Type 'Skip' to quit this operation cycle ~ ----------\n")
    ################################################################################
    ################################ [4] Daily Recommendations######################
    ################################################################################
    boolean_str = input("STEP_4 to STEP_6 ---> VIP SERVICE: PERSONALIZED RECOMMENDATION (e.g. subscribe or refuse)")
    if boolean_str == "subscribe":
        print("\n-------------------------------\n")
        print("[STEP_4] DAILY PLAYLIST RECOMMENDATIONS ...")
        print("THE NAME OF PLAYLIST\t\t\t\t\t\t |THE PLAYLIST ID")
        daily_recommendation = daily_recommendation(identify_cookie)['recommend']
        for items in daily_recommendation:
            english_translated_text = Supporting_Func.translate_text(items['name'], 'en')
            print("{:<25}\t\t\t{:<16}".format(english_translated_text, items['id']))

        print("\n-------------------------------\n")
        print("[STEP_5] GET RECOMMENDATIONS ABOUT ARTIST...")
        recommendations_result = get_recommendation()['result']
        ID_LIST = []
        for item in recommendations_result:
            song = item['song']
            album = song['album']
            print("{:<16}".format(Supporting_Func.translate_text(album['artists'][0]['name'], 'en')))
            ID_LIST.append(song['id'])

        print("\n-------------------------------\n")
        print("[STEP_6] GET SONGS OF THE RECOMMENDED ARTISTS...")
        for ID in ID_LIST:
            result = get_songs_from_artists(ID)['songs']
            print(f"------ID:{ID}------")
            print("{:<25}\t|{:<16}\t|{:<16}".format("NAME", "ID", "ARTIST"))
            for item in result:
                english_translated_name = Supporting_Func.translate_text(item['name'],'en')
                english_translated_artists = Supporting_Func.translate_text(item['artists'][0]['name'],'en')
                print("{:<25}\t{:<16}\t{:<16}".format(english_translated_name, item['id'], english_translated_artists))

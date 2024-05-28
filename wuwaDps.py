from datetime import datetime
import time
import time as timesleep
import os

#live / history
usage = 'live'

while True:
    entities = {} #entityId1:[hp:None, dps10s:None], entityId2:[hp:None, dps10s:None], ...
    logsFile = None
    lines = None
    try:
        logsFile = open('C:\Wuthering Waves\Wuthering Waves Game\Client\Saved\Logs\Client.log', 'r', encoding="utf-8")
        lines = logsFile.readlines()
    except:
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        logsFile.close()
        timesleep.sleep(0.2)
        continue

    #[2024.03.04-09.05.05:247][446][GameThread]Puerts: Display: (0x000000003F316DF0)
    #[68775][I][CombatInfo][WCL][49504][9.5.5:246] [Part][EntityId:233086:Monster:BP_ME1BinlangMd00601_C_2147390678]
    #UpdatePartInfo [TagName: 怪物.common.背部弱点][Activated: true][LifeValue: 9858]

    if usage=='live':
        currentTime = datetime.now()

    for i in range(len(lines)-1,-1,-1):
        #'CombatInfo' in lines[i] and
        if 'LifeValue' in lines[i]:
            # print(lines[i].partition('LifeValue: ')[2].partition(']')[0])
            pastHp = float(lines[i].partition('LifeValue: ')[2].partition(']')[0])
            entityId = lines[i].partition('[EntityId:')[2].partition(':')[0]

            #                                       2024.03.04-09.05.05:247
            time = datetime.strptime(lines[i][1:24], "%Y.%m.%d-%H.%M.%S:%f")
            #if usage=='live' and (currentTime - time).seconds > 60:
                #break

            if entityId not in entities:
                entities[entityId] = {}
                entities[entityId]['hp'] = pastHp
                entities[entityId]['name'] = lines[i].partition('Monster:BP_')[2].partition('_')[0]
                entities[entityId]['lastCombatTime'] = time


            #print('entityId: '+entityId)
            #print('time: '+str((currentTime - time).seconds))
            #print('hp: '+str(pastHp)+', '+str(entities[entityId]['hp'])+'\n\n')

            if (currentTime - time).seconds < 10 and (currentTime - time).seconds > 0:
                entities[entityId]['dps10s'] = (pastHp - entities[entityId]['hp']) / (currentTime - time).seconds
            if (currentTime - time).seconds < 60 and (currentTime - time).seconds > 0:
                entities[entityId]['dps60s'] = (pastHp - entities[entityId]['hp']) / (currentTime - time).seconds

            if (entities[entityId]['lastCombatTime'] - time).seconds != 0:
                entities[entityId]['dpsOnThatEnemy'] = (pastHp - entities[entityId]['hp']) / (entities[entityId]['lastCombatTime'] - time).seconds

    # output
    if usage=='live':
        os.system("cls")
        print('10s dps:')
        for entityId in entities.keys():
            entity = entities[entityId]
            if 'dps10s' in entity:
                if entity['dps10s'] != 0:
                    #print('   '+entity['lastCombatTime'].strftime("%H:%M:%S"))
                    print('   '+entityId+':'+entity['name']+'\t: '+str(int(entity['dps10s'])))

        print('60s dps:')
        for entityId in entities.keys():
            entity = entities[entityId]
            if 'dps60s' in entity:
                if entity['dps60s'] != 0:
                    #print('   '+entity['lastCombatTime'].strftime("%H:%M:%S"))
                    print('   '+entityId+':'+entity['name']+'\t: '+str(int(entity['dps60s'])))

    print('history:')
    for entityId in entities.keys():
        entity = entities[entityId]
        if 'dpsOnThatEnemy' in entity:
            if entity['dpsOnThatEnemy'] != 0:
                print('   '+entity['lastCombatTime'].strftime("%H:%M:%S"))
                print('   '+entityId+':'+entity['name']+'\t: '+str(int(entity['dpsOnThatEnemy'])))


    timesleep.sleep(0.2)

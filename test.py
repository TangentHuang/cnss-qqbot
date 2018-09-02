# coding=utf-8
from cqhttp import CQHttp
import re
import sys
import argparse
import requests
import traceback

bot = CQHttp(api_root='')
pigeon= False
group_list=(253370800,781269903,808234958)
power_list=(895853325,)
welcomeList=[]

welcome_newbie= "Hi，欢迎加入 CNSS 2018 招新群 XD \n\n "\
                "请先阅读以下事项：\n\n" \
                "* 夏令营平台: summer.cnss.io\n\n"\
                "* 为了让大家更好的相互了解，请先阅读群公告本群须知，更改一下群名片\n"\
                "* 如有任何疑问，请在群里艾特管理员提问"
why_at_me="为啥AT我？咕咕咕~"
power_at_me="大哥好~我只是一只小鸽子"
card_pattern = R"\d{2}[-].*"

def check_group_card():
    try:
        info = bot.get_group_member_list(group_id=781269903)
        to_shot_list = []
        to_shot_msg = ''
        for each in info:
            member = bot.get_group_member_info(group_id=int(each['group_id']), user_id=int(each['user_id']),no_cache=False)
            card = member['card']
            print(card)
            if not re.match(card_pattern, card):
                to_shot_list.append(member)
        for each in to_shot_list:
            to_shot_msg+= ('[CQ:at,qq=%d]'% each['user_id'])
        to_shot_msg+='\n群名片不符合规范，请参照格式更改'
        bot.send_group_msg(group_id=253370800,message=to_shot_msg) #bot messsage群
    except:
        print('check_group_card error')


def check(context):  #检测群
    group=context.get('group_id')
    person=context.get('user_id')
    if group in group_list:
        print("botMessage")
        return True
    return False

def check_man(context):  #检测powerMan
    person=context.get('user_id')
    if person in power_list:
        return True
    return False

def switch_pigeon(pigeon): #复读模式切换
    if pigeon:
        return False
    else:
        return True


def menu(context):
    menu_list = "施工中ing 请耐心等待"

    context['message'] = context['message'].strip()
    context['message_no_CQ'] = re.sub(R'\[CQ:[^\]]*\]', '', context['message']) #去除CQ码
    context['message_no_CQ']=context['message_no_CQ'].strip()
    print(context['message_no_CQ'])
    if not (context['message'] and context['message_no_CQ'][0] in ('-',)):
        bot.send(context,power_at_me)
        return
    if '-h' in context['message_no_CQ']:
        bot.send(context, message=menu_list)
        return
    if '-checkCard' in context['message_no_CQ']:
        check_group_card()
        return
    bot.send(context,power_at_me)
    return



@bot.on_message('private','group')
def handle_msg(context):
    is_group=bool(context.get('group_id'))
    if is_group:
        at_me = '[CQ:at,qq=%d]' % 1751065040  # 机器人被@
        if at_me in context['message']:
            at = '[CQ:at,qq=%d] ' % context['user_id']
            if not check_man(context):
                bot.send(context,why_at_me)
            else:
                menu(context)
        if check(context) and pigeon:
            print(context)
            return {'reply': context['message'], 'at_sender': False}
        if "鸽" in context['message']:
            return {'reply':"咕咕咕",'at_sender':False}
        return

@bot.on_notice('group_increase')
def handle_group_increase(context):
    if check(context):
        print(context)
        welcomeList.append(context['user_id'])
        welcomMessage= ''
        if len(welcomeList) == 6 :
            for each in welcomeList:
                at = ('[CQ:at,qq=%d] ' % each)
                welcomMessage += at
            group = context.get('group_id')
            bot.send_group_msg(group_id=group, message=welcomMessage+welcome_newbie)
            welcomeList.clear()
        print(context['user_id'])
        #bot.send(context, message=at+welcome_newbie,is_raw=False)  # 发送欢迎新人
    return

@bot.on_request('group', 'friend')
def handle_request(context):
    return {'approve': True}  # 同意所有加群、加好友请求

bot.run(host='0.0.0.0',port=8080)

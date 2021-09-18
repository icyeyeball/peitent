# -*- coding: utf-8 -*-
############################
# Peicheng Lu 20190822
############################
# Usage: python _compare.py 
import sys
import re
#demo.py must be utf-8
import gensim
import numpy
import jieba
import math

def sort_by_value(d): 
    items=d.items() 
    backitems=[[v[1],v[0]] for v in items] 
    backitems.sort()
    return [ backitems[i][1] for i in range(len(backitems)-1, -1, -1)]

class_l = {
    1:"工業、科學、照相用,以及農業、園藝、林業用之化學品;未加工人造樹脂、未加工塑膠;滅火及防火製劑;回火及焊接製劑;為鞣製獸皮及皮革用鞣劑;工業用黏著劑;油灰及其他糊狀填充劑;堆肥、動物性肥料、化學肥料;工業及科學用生物製劑。",
    2:"漆、清漆、亮光漆;防銹劑及木材防腐劑;著色劑、染料;印刷、打印及雕版用油墨;未加工天然樹脂;塗裝、裝潢、印刷與藝術用金屬箔及金屬粉。",
    3:"不含藥化粧品及盥洗用製劑;不含藥牙膏、牙粉;香料、香精油;洗衣用 漂白劑;清潔劑、擦亮劑、洗擦劑及研磨劑。",
    4:"工業用油及油脂、蠟;潤滑劑;灰塵吸收劑、灰塵濕潤劑及灰塵黏著劑;燃料及照明用燃料;照明用蠟燭、燈芯。",
    5:"藥品、醫療用及獸醫用製劑;醫療用衛生製劑;醫療用或獸醫用食療食品、嬰兒食品;人用及動物用膳食補充品;膏藥、敷藥用材料;填牙材料、牙蠟;消毒劑;殺蟲劑;殺真菌劑、除草劑。",
    6:"普通金屬及其合金、礦砂;建築及結構工程用金屬材料;可移動金屬建築物;普通金屬製非電氣用纜索及金屬線;小五金;貯藏或運輸用金屬製容器;保險箱。",
    7:"機器、工具機、電動工具;非陸上交通工具用馬達及引擎;非陸上交通工具用機器聯結器及傳動零件;手動手工具除外之農具;孵卵器;自動販賣機。",
    8:"手動式手工用具及器具;刀叉匙餐具;非槍砲之隨身武器;剃刀。",
    9:"科學、研究、導航、測量、攝影、電影、視聽、光學、計重、計量、信號、檢測、測試、檢查、救生和教學裝置及儀器;電力分配或使用之傳導、切換、轉換、蓄積、調節或控制用裝置及儀器;聲音、影像或資料之記錄、傳送、複製或處理用裝置及儀器;已錄和可下載之媒體、電腦軟體、空白數位或類比錄製及儲存媒體;投幣啟動設備之機械裝置;收銀機、計算裝置;電腦和電腦週邊設備;潛水衣、潛水面鏡、潛水用耳塞、潛水及游泳用鼻夾、潛水手套、潛水用呼吸裝置;滅火裝置。",
    10:"外科、內科、牙科與獸醫用之器具及儀器;義肢、義眼、假牙;矯形用品;傷口縫合材料;傷殘人士適用之治療及輔助裝置;按摩器具;哺乳嬰兒用器具、裝置及物品;性活動用器具、裝置及物品。",
    11:"照明、加熱、冷卻、產生蒸氣、烹飪、乾燥、通風、給水及衛浴設備和裝置。",
    12:"交通工具;陸運、空運或水運用器械。",
    13:"火器;火藥及發射體;爆炸物;煙火。",
    14:"貴重金屬及其合金;首飾,寶石及半寶石;鐘錶和計時儀器。",
    15:"樂器;樂譜架及樂器支架;指揮棒。",
    16:"紙及紙板;印刷品;裝訂材料;照片;家具除外之文具及辦公用品;文具用或家庭用黏著劑;繪畫用具及藝術家用材料;畫筆;教導及教學用品;包裝用塑料片、薄膜及袋;印刷鉛字、打印塊。",
    17:"未加工及半加工之橡膠、馬來樹膠、樹膠、石棉、雲母及該等材料之替代品;生產時使用之擠壓成型塑膠及樹脂;包裝、填塞與絕緣材料;非金屬製可彎曲之輸送管、管及軟管。",
    18:"皮革及人造皮革;動物皮及獸皮;行李袋及手提袋;傘及遮陽傘;手杖;鞭子、馬具;動物用項圈、牽繫用帶及衣服。",
    19:"非金屬製建築材料;建築用非金屬製硬管;柏油、瀝青;非金屬製可移動之建築物;非金屬製紀念碑。",
    20:"家具、鏡子、畫框;貯藏或運輸用非金屬製容器;未加工或半加工之骨、角、鯨骨或珍珠母;貝殼;海泡石;黃琥珀。",
    21:"家庭或廚房用具及容器;餐叉、餐刀及餐匙以外之烹飪用具及餐具;梳子及海綿;畫筆除外之刷子;製刷材料;清潔用具;除建築用玻璃外之未加工或半加工玻璃;玻璃器皿、瓷器及陶器。",
    22:"繩索及細繩;網;帳蓬及塗焦油或蠟之防水篷布;紡織品或合成材料製之遮篷;帆;運輸及貯藏散裝貨物用粗布袋;紙、紙板、橡膠或塑膠除外之襯墊、減震及填塞材料;紡織用纖維原料及其替代品。",
    23:"紡織用紗及線。",
    24:"紡織品及紡織品替代品;家用亞麻布製品;紡織品製或塑膠製簾。",
    25:"衣著、靴鞋、頭部穿戴物。",
    26:"類:花邊、辮帶及刺繡品,以及裁縫用品飾帶及蝴蝶結;鈕扣、鉤扣、別針及針;人造花;髮飾品;假髮。",
    27:"地毯、小地毯、地墊及草蓆、亞麻油地氈及其他鋪地板用品;非紡織品製壁掛。",
    28:"競賽遊戲用品、玩具及遊戲器具;視頻遊戲器具;體操及運動用品;聖誕樹裝飾品。",
    29:"肉、魚肉、家禽肉及野味;濃縮肉汁;經保存處理、冷凍、乾製及烹調之水果及蔬菜;果凍、果醬、蜜餞;蛋;乳、乳酪、奶油、酸乳酪及其他乳製品;食品用油及油脂。",
    30:"咖啡、茶、可可及代用咖啡;米、義大利麵條及麵條;樹薯粉及西谷米;麵粉及穀類調製品;麵包、糕點及糖果;巧克力;冰淇淋、水果雪泥冰及其他食用冰;糖、蜂蜜、糖漿;酵母、發酵粉;鹽、調味料、調味用香料、經保存處理的香草;醋、調味醬及其他調味品;冰(結冰水)。",
    31:"未加工農業、水產養殖、園藝及林業產品;未加工穀物及種子;新鮮水果及蔬菜,新鮮香草;天然植物及花卉;球莖,植物種苗及植栽用種子;活動物;動物用飼料及飲料;釀酒麥芽。",
    32:"啤酒;不含酒精之飲料;礦泉水與汽水;水果飲料及果汁;製飲料用糖漿及其他製飲料用不含酒精之調製品。",
    33:"酒精飲料;製飲料用含酒精之調製品。",
    34:"菸草及菸草代用品;菸及雪茄;電子菸及吸菸用霧化器;菸具;火柴。",
    35:"廣告;企業管理;企業經營;辦公事務。",
    36:"保險;財務;金融業務;不動產業務。",
    37:"建築物建造;修繕;安裝服務。",
    38:"電信通訊。",
    39:"運輸;貨品包裝及倉儲;旅行安排。",
    40:"材料處理。",
    41:"教育;提供訓練;娛樂;運動及文化活動。",
    42:"科學及技術性服務與研究及其相關之設計;工業分析及工業研究服務;電腦硬體、軟體之設計及開發。",
    43:"提供食物及飲料之服務;臨時住宿。",
    44:"醫療服務;獸醫服務;為人類或動物之衛生及美容服務;農業、園藝及林業服務。",
    45:"法律服務;對有體財產和個人提供實體保護之安全服務;為配合個人需求由他人所提供之私人或社交服務。"
}

jieba.set_dictionary('../jieba_dict/dict.txt_new.big')

model = gensim.models.Word2Vec.load('../word2vec_20190801.model')
#with open('./class/1.txt','r', encoding='utf-8') as f:
tmp = 0.
weight = 0.
weight_d = {}
input = sys.argv[1]
input_l = []

for i in range(0,len(input)):
    for j in range(0,len(input)-i):
        try:
            semi = model.wv.most_similar(input[j:j+i+1])
        except KeyError:
             continue
        else:
            print(input[j:j+i+1])
            input_l.append(input[j:j+i+1])
            if len(input_l) > 4:
                del input_l[1]

for k in range(0,45):
    with open('./class_final_t/' + str(k+1) + '.txt', 'r', encoding='utf-8') as f2 :
        weight_l = []
        for texts_num, line in enumerate(f2):
            words = jieba.cut_for_search(line)
            for word in words:
                try:
                    semi = model.wv.most_similar(word)
                except KeyError:
                    continue
                else:
                    #print ("OOOOOOO word " + word)
                    for i in range(0, len(input_l)):
                        try:
                            semi = model.similarity(word, input_l[i])
                        except KeyError:
                            continue
                        else:
                            tmp = model.similarity(word, input_l[i])
                            if tmp > 1:
                                tmp = 1
                            #print ("=== tmp = " + str(tmp))
                            weight_l.append(tmp)
                            
                            for a in range(0,len(weight_l)-1): 
                                for b in range(0,len(weight_l)-1-a): 
                                    if weight_l[b] < weight_l[b+1]: 
                                        tmp = weight_l[b]
                                        weight_l[b] = weight_l[b+1]
                                        weight_l[b+1] = tmp
                            if len(weight_l) > 3:
                                del weight_l[3]
    total = 0.0
    for a in range(0,3):
        print (math.degrees(math.acos(weight_l[a])))
        print("相似度 = " + str((math.degrees(math.acos(weight_l[a]))*(-0.55555556)) +100.) + "%")
        total += (math.degrees(math.acos(weight_l[a]))*(-0.55555556)) +100.
    weight_d[k+1] = total
    total  = total / 3.
    print ("k = " + str(k+1) + "  total = " + str(total))
result_l = sort_by_value(weight_d)
for i in result_l:
    print ("第"+ str(i) +"類 : ")
    print ("   "+class_l[i])

            #print (word)
            #print (model.similarity(sys.argv[1], word))
            #print ("==============")




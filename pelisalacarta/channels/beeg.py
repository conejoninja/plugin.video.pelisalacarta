# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para beeg.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por aampudia
#------------------------------------------------------------
import cookielib
import urlparse,urllib2,urllib,re
import os
import sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "beeg"
DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[beeg.py] mainlist")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="videos"            , title="Útimos videos"       , url="http://beeg.com/"))
    itemlist.append( Item(channel=__channel__, action="listcategorias"    , title="Listado categorias"  , url="http://beeg.com/"))
    itemlist.append( Item(channel=__channel__, action="search"            , title="Buscar"              , url="http://beeg.com/search?q=" ))
    return itemlist

def videos(item):
    logger.info("[beeg.py] videos")
    data = scrapertools.downloadpageWithoutCookies(item.url)
    itemlist = []

    '''
    var tumbid  =[7208081,1022338,1790112,2909082,2410088,8691046,8462396,2014246,8808325,4654327,8062507,7000421,8548437,1767501,6295658,3202102,2773864,9612377,6948607,9943885,5264590,6982322,6165308,9324770,3619002,8925867,5368729,1082464,5214883,8294614,4242507,3240149,4273919,4475499,4804736,8587147,8338151,1038421,1004169,9272512,5305005,5083086,3580156,1874869,9885579,1058926,3174150,1066977,7082903,6530464,4624902,8591759,6102947,4657695,2016527,6577806,2239334,9870613,2440544,8152565,8219890,3030145,8639777,9848873,7349742,2950534,7119152,5997556,2374574,9815315,3214267,5432670,4658434,4580658,8404386,7524628,4124549,4927484,4181863,9276920,2495618,9318916,6860913,1513045,4236984,6061992,4609004,5271124,5401171,8848711,6836799,1980560,4589392,8210830,8490012,5932132,4250379,2306395,1792556,2148371,1700509,5098703,9776305,7905694,4203280,4423411,6712077,9004474,1402706,4263429,5198666,9395866,5457900,4030776,8735416,9222101,5131412,9355090,5153675,3461256,3701598,9727360,3618152,6070007,7335171,5410904,1947651,5306023,6515828,3715868,7608229,3489585,7264184,7743498,3397575,3511213,6619182,7876772,8770245,8093453,7989500,1961547,5522799,6588700,4531347,1437017,2219295,4546557,6982198,2939794,2298045,8080263,7128768,2765167,2319077,9522842,4961084,5604127,9955979,5111810,4778525,6692226,5511006,9344899,4803658,6146385,1775954,4516958,2634309,1630574,4615420,6358106,6047503,6682604,4328147,8154411,7774060,2064366,3405726,5325432,6587525,9334690,8067415,8027270,1138550,4367956,8382277,1024046,4306081,9228857,7817771,6926228,6303685,7710118,4647190,4017796,9559557,5766637,3330727,1944600,5188555,5726903,6942768,4986192,8708803,6080195,9399238,7572599,3186224,4224246,2932085,5380191,3088447,5901127,3887214,2349737,5714776,2563377,4038474,8499863,4227950,6499672,6991633,3024612,6814845,6454321,2843677,8396005,7907216,1301562,8709563,5458247,9226733,8557509,7207699,1922207,1490492,5647366,1591222,8846795,4011662,1303847,3537608,2412365,4457772,9007518,4005900,4225550,8399634,4685661,5839323,7256007,1743108,6664595,9449274,7988727,3676039,4539781,5606635,7285872,5784054,3700937,4002132,1327636,1308207,7921776,4890112,1034360,4438762,7616608,1546748,1764556,7211306,9832815,8328351,7392273,9392812,9536883,3429689,1129731,4112108,6680341,1587601,3872723,7753727,4238235,8065294,6601466,7435260,9834733,6962573,4507291,7187479,8365423,9132777,2375411,2758884,5054277,6612817,2448785,5836846,6353814,6049471,7341687,1989319,4013602,4660258,1981692,5649634,7315856,9405860,6398978,4517613,1315807,8808025,8442117,2160975,5989886,3924302,7065269,8475308,8586280,3215143,4277208,7310326,7217778,7465561,7512526,3067747,8028981,8436023,6517768,5466318,9613743,6767061,3712249,4986686,3187636,3248477,8212121,2837620,8563996,3689648,5153513,5646012,3979442,3023435,3606043,1521306,2602755,7371342,5113191,4669626,1560957,9490908,6871729,2327539,5035151,7543878,3937587];
    var tumbalt =['She gives a blowjob and pussy before she goes to work','Toga Orgy! Tits, Asses and Blowjob','Cute cocksucker','Cute fresh girl fucking and taking facial cumshot','Russian girl playing with her pussy','Euro amateur wife fucking on camera','I work with my pussy','Take your clothes off for money.., now','Because I\'ve paid her for sex','Rear stuffing','A company for casual sex','Getting wet by the pool','Shyla Jennings & Avril Hall','Pervert Eva anal toying on webcamera','Group sex with her step-mom','Blonde, brunette and a guy','Blonde natural titted Jessica','Lick mommy\'s pussy first','Pretty with perfect ass fucking and taking facial','Hardcore sex n the club, in front of public','Black girl with booty that she is not afraid to suck for the cam','Tanned blonde teen fycking by the pool side','Prof. Tate letting her student fuck her pussy','Crew Appreciation','Condition of the apartment','Fucking this round ass after two nights in jail','Anjelica & Momoko','Because Tiffany is fucking awesome','I\'m rested and ready to fuck Eva Angelina','Money Talks crew is taking care of a fur coat shop','Long legged blonde Euro girl Ivana','Dos Buenos','Cute massagist fucking and taking facial cumshot','A petulant young woman','Young skinny Zoey wants it big','I have absolutely no problem having sex for money','Cutie with natural tits getting fucked','Masturbating Jasmin','Don\'t worry! It\'s just a fuck','Amateur Yasmine spreading and masturbating on camera','Super cute with amazing body getting fucked','Young busty gets her perfect ass fucked by 2 big black cocks','Russian amateur girl playing with pussy and ass','Homemade video. Natural titted wife gets fucked from behind','Hottie getting fucked in nature','Shake that Ass babe! Shake that Ass!','Bang Me','Sweet ass sugar','Biking booty','Moans and facial "expressions"','Sunset Love','An extra credit assignment','No choice but to eat out each others pussies','Party Pussy','Facial Interview','Lesbian teens playing with their asses','Not a problem... you can fuck my girlfriend...','Women are waaaaay worse!','Lesbian neighbors','Big titted Vanilla DeVille getting facial cumshot','Fulfilling MILF\'s fantasies','Picked up, fucked and creamed','Teens having group sex party','Heart Line reveals she\'s a true slut','Tracey Sweet','Kitchen Doll','Classy fuck party at the dorm','Angel in white sexy lingerie','I jumped on the opportunity to fuck Brandi Love','I\'m finally ready to do it!','Brittany\'s sex tape. Big round beautiful silicone tits','Sharing the house','Testing Ashlynn','Lorena, Penelope, Cock','Take the money and put this cock in your teen mouth','-','Cut and suck some wood','Romantic Oral','Podcast. Girl getting fucked on webcamera','Alone and horny','Tattooed girlfriend gets fucked on a kitchen table','Late to class?','Punished by a cock','tied and ass fucked','A French girl surprise','Innocent Asian gets her ass fucked by two. Creampie','Young couple in bed','She invites him for... a blowjob','Pretty busty Euro teen playing with her ass on camera','Vacation Sex','Toying teens','Top dance instructor','Birthday Video','Elainas step mom, Diana, joined the action','Havoc has good tits and loves good tits','Loving her lesbian friend while her bf fucks her from behind','Fucking mom in front of her step-daughter','Charlotte & Paloma giving head','The Sweethearts prestigious Title','Kris does exactly as he\'s told','Brought to the apartmen','Alicia is a bubbly redhead with loads of personality','Nadin & Stephanie share a cock','Young blonde petite Ella','Young amateur couple making a creampie','Taking my aggression out on some pussy... or face','Drink my sweet pussy milk','No problem fucking my sugar daddy','18 yo Shay giving head on camera','Brooklyn Dayne','Young couple','Hottie getting fucked in public','18 years old massagist','Sierra, and Kenzie get fucked','Ramon is Cast Into Hellfire','Lick our college pussies until we cum! Orgy.','Looking for a cowgirl to ride her pony','Dick in Mrs. Lynn\'s mouth, tongue in her pussy','Caprice','Gorgeous French lesbians','Bysty amateur girl masturbating on camera','Lady\'s night hardcore','Vagina Golf','Hardcored on a sofa','Sucking and fucking his his criminal cock','Exploiting her roommate\'s slutty behavior','Crew Appreciation','Czech cutie with a nice couple of tits getting fucked','Orgy in Roman style','Send your boyfriend home','Beautiful Russian Valeria masturbating on camera','Sexual Tendencies','Young couple in homemade hardcore video','Lezley Zen gets fucked hard from behind','A tall slender blonde for the fiesta!','Teen with Juggs from Heaven','Between us','I have two jobs','Young Mandy Sky fucking','18 year old butthole ride','Some strategizing of her own','Girly Passion','She was ready to go','Brooklyn gets her pussy munched and fucked','To help her out','MILF from Barcelona!','Zoey goes Big','Its official!','German granny in action','Shyla and Avril','College sex life','European country girl gets bend over the table and fucked','Gangbanged by Five','In my hotel room','Letting her student eat her pussy','Long legged Ivana Interested in renting with her pussy','Skinny Stephanie in doggy style','Twist Game','Professional Lesbians','Amateur Fuck','Fuck with great pleasure','Summer gets a pussy pounding','Young teaser','Prance around show off their asses and pussies','Read my Cunt','Young with big beautiful natural tits','Busty blonde patient gets fucked','A banging ass','Lady\'s night blow out','Delicious Lesbians','Because I\'ve paid for it','Sunset Love','Young Rita with juggs from Heaven','Amateur blonde masturbating on camera','Pole Smoker','Polish GF with big natural tits fucking on camera','Nurse having sex with patient','She\'ll be tested on this week','Alicia needs money immediately','The Girls School the Newbs','To give you an idea of how fun she is...','I\'m just one of her clients','Cute Katie massaging my cock with her pussy','A Milf that keeps on giving','I just love to fuck hot women','She\'s dating my father','I am never letting my girl go to a strip!','Kymber Lee needs her pussy wet!','Pornstar fucking at a sex shop','My pussy got pranked','Euro teen with big beautiful natural tits fucking','Toying and fucking beautiful round ass','Shy Asian sweetie giving head and taking facial cumshot','Why don\'t you do that to my cock?','Eat this pussy Milk','Amazing Beauties. No sex','Mom gets fucked in front of her step-daughter','Hardcore Pranking','Cute Czech girl gets taken home and fucked','A shady office at night time','Party Asses','I paid this chick good money','Body of Brooklyn','Girls riding the cruisers','Blondie Boom gets it in doggy style','Sex Instruction','College Rituals','Tied up and helpless. No sex','Too big for my teen ass','Classroom Hardcore','Amateur couple licking, sucking, fucking and cumming!','Emergency help with anal sex','Redhead Euro MILF with big tits and good ass in action','A classy party at the dorm','Lick my teen pussy','Hot Latin chick gets banged by dancing bear','OK, I have her now!','Florida Students','Pussy Business','Czech girl with big natural tits gets fucked on a sofa','Four lesbians in Love','Moms set pounded too','My husband lost his job.., I\'m going to work','Long legged professionals with good asses share a cock','Sunset Lesbian Nymphos','Shy Japanese teen getting fucked on camera','Strip girl getting her ass fucked by two','Educated women','Money Talks XXX experiments','Jada goes to his office','Busty teacher letting him fuck her','To fuck his brains out','Party Pussy','The economics of modeling','Girl to guy ratio seems to be out of whack','Of course I wanted to fuck','Young blonde beautiful massagist','Fucking his neighbor','Zoey goes Big','Schoolgirl taking cock','A classy party at the dorm','On the kitchen table','Sex in sauna','I want to fuck her hard','Young amateur couple fucking in bathroom and bedroom','Rear stuffing','Respect for educated women','Tattooed lesbians on a bed','Amateur 19 year old girlfriend giving head','Teen couple','On our way to the office...','Pumping energy into a teacher','Cute teen gets fucked in her bed','Orgy in a club','A new college course','I need to take my aggression out on some pussy','In doggy style','Dance, Dance, Fornication','Dating service for female millionaires','A little cheerleader gets fucked','In his parents\' bedroom','Strip Poker','Crazy group of ladies','And I get to fuck her. Why? Bc I\'ve paid for it!','Her boyfriend was not satisfying her','Super beautiful amateur teen fucking on camera','The Art','Hardcore in a dorm','We\'re actually lucky to have Tiffany','The Economics of Modeling','The sisters order','With help of Mrs. Avluv','Angelina gives great head','Alone, and in my hotel room','To see my new college counselor','Super skinny Stephanie giving head','He pays for everything that my husband can\'t','Milf with big natural boobs getting fucked','We got cash for your tits','GF getting fucked in many positions','Asa Akira in action','I fucked my step-mom in doggy style','Hotel Cockafornia','They have their own party','Big black cock inside inside his step-mom\'s wet pussy','Amateur girls get fucked on camera, in doggy style','Blonde teen with perfect ass','A tall slender blonde with blue eyes','Magic Box','My teacher letting me fuck her','Victoria rides my dick','Little cheerleader','A big big favor for a nice nice neighbor','Blow Job Frenzy','Crazy group of ladies. No sex','We fertilize her vagina with some magic seeds','Blonde teens on a cock','Sophie & Sasha in college threesome','Hottie With a Body','A company for casual sex','I\'m into her','Young beautiful sexy massagist','Black babe having sex in different places','Lesbian Maids','Jessica Jaymes','Two hot Milfs share a cock','Signing up for a new class at college','Teen goes Big','Kenzie & Sierra getting assfucked','Ride with Tracey Sweet','Show Me Your Pussy','Long legged babe with amazing body in hardcore','Amateur blonde gets her Big Natural Tits fucked','A new college course','Tits for the password','Long haired brunette in lingerie fucking','Angela & Luiza','That\'s why I\'ve paid for Lezley Zen','Until she gets foam on her face','Amateur couple fucking on camera','Tits & Asses. No sex','Another wonderful day','Beautiful Lizz Tayler fucking and swallowing','She doesn\'t want him to be lonely','Chloe is a dirty little schoolgirl','All Blonde','Cleaning so to speak','Fuck my tits and my ass','Unable to resist my step-mom\'s sexy French charms','Cum on my step-mom\'s face','An artist looking for a model to paint','Girls fucking, boys watching','Blonde schoolgirl gets her ass fucked and takes facial cumshot','18 yo teen having sex in her room','Feel the hotness','Because her boyfriend was not satisfying her','She needs to fuck for this audition to continue','Big ass amateur redhead gets fucked by her step son','Dorm Life','I\'ve paid for Amy Brooke tonight','Tonight I cum on Priya Anjali Rai\'s face','So he can do well on his test','Mommy takes care of it','Tied and fucked hard by two','You win my cock','Beauty with perfectly round ass fucking and taking facial for money','Hot ass Deborah paying the rent with her pussy','They have their own party','The woman in the middle','18 yo Shay decides to shoot her first porn movie','Blow Job Frenzy','Young busty Haley meets the Beast of Cock','Sex Instruction','Signing up for a new class at college','Read my Cunt','Creaming her pretty pussy. Meggan is stoked to leave laid and paid!','Small Pussy, Big Package','Would it be rude to ejaculate on my girlfriend\'s face?','Port of Cock, New Whoreleans','He pounds his girlfriend\'s tight pussy on camera'];
    var writestr = '<div id="thumbs">';
    var URLthumb = 'http://beeg.com/';
    var IMGthumb = 'http://eu1.anythumb.com/236x177/';
    '''
    
    base_thumbnail_url = scrapertools.get_match(data,"var IMGthumb \= '([^']+)'")
    base_url = scrapertools.get_match(data,"var URLthumb \= '([^']+)'")
    base_url = urlparse.urljoin("http://beeg.com/",base_url)

    # Lista de IDs
    id_list = []
    id_string = scrapertools.get_match(data,"var tumbid  =\[([^\]]+)\]")
    
    patron="(\d+)"
    matches = re.compile(patron,re.DOTALL).findall(id_string)
    
    for match in matches:
        id_list.append(match)

    # Lista de titulos
    title_list = []
    title_string = scrapertools.get_match(data,"var tumbalt \=\[([^\]]+)\]")
    
    title_string = title_string.replace("\\'",'"')
    patron="'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(title_string)
    
    for match in matches:
        title_list.append(match)

    for i in range(0,len(id_list)):
        try:
            scrapedtitle = unicode( title_list[i], "utf-8" ).encode("iso-8859-1")
        except:
            scrapedtitle = title_list[i]
        scrapedtitle = scrapedtitle.replace('"',"'")
        scrapedurl =  base_url+id_list[i]
        scrapedthumbnail = base_thumbnail_url+id_list[i]+".jpg"
        scrapedplot = ""
        # Depuracion
        if (DEBUG): logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")            
        itemlist.append( Item(channel=__channel__, action="play" , title=scrapedtitle , url=scrapedurl, thumbnail=scrapedthumbnail, plot=scrapedplot, show=scrapedtitle, viewmode="movie", folder=False))
    
    return itemlist

def listcategorias(item):
    logger.info("[beeg.py] listcategorias")
    data = scrapertools.downloadpageGzip(item.url)
    data = scrapertools.get_match(data,'<div class="block block-tags">(.*?)<!-- /TAGS -->')
    patron = '<li><a target="_self" href="([^"]+)" >([^"]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    for url, categoria in matches:
      url= "http://beeg.com" + url
      itemlist.append( Item(channel=__channel__, action="videos" , title=categoria, url=url))
      
    return itemlist
  
def search(item,texto):
    logger.info("[beeg.py] search")
    texto = texto.replace(" ","+")
    item.url = item.url+texto
    try:
        return videos(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def play(item):
    logger.info("[beeg.py] play")
    itemlist = []
    data = scrapertools.downloadpageGzip(item.url)
    if DEBUG: logger.info(data)
    patron = "'file'\: '([^']+)'"
    url = scrapertools.get_match(data,patron)
    itemlist.append( Item(channel=__channel__, action="play" , title=item.title , url=url, thumbnail=item.thumbnail, server="directo", folder=False))

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    # mainlist
    mainlist_items = mainlist(Item())
    videos_items = videos(mainlist_items[0])
    play_items = play(videos_items[0])

    if len(play_items)==0:
        return False

    return True

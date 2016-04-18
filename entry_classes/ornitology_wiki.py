# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 15:20:16 2016

@author: misha
"""

from tools.sr_lat2cyr2lat import *
from collections import Counter
import os, re


REFERENCES = {
"АПГС" : "Слободан Пузовић – Братислав Грубач – Хам Иштван – Саша Маринковић – Јавор Рашајски – Биљана Ковачев – Ђорђе Томић – Жељко Станимировић – Марјан Никетић, Атлас птица грабљивица Србије, Завод за заштиту природе Србије, Нови Београд – Нови Сад – Приштина – Ниш 2000.",
"АСК" : "Милош Кордић, Азбучник села Комоговине, СКД Просвјета, Загреб 2014.",
"Арс. В." : "Владан Арсенијевић, Јестаственица (за учитељске и више девојачке школе), део 1, Зоологија, Нови Сад 1879.",
"Бар. П." : "П. Баришић, Дивљач и лов у Босни и Херцеговини, Шумарски лист, орган хрват.-славонскога шумарскога друштва, бр. 2. год. IX, Загреб 1885, 57–61.",
"Бен. Е." : "Емил Бенић, Обедска бара и њена главна фауна, Штампарија браће Јанковића, Сремска Митровица 1930.",
"Богд. Н." : "Недељко Богдановић, Лексика у Белићевим Дијалектима источне и јужне Србије, Годишњак за српски језик, год. XXVI, бр. 13, Филозофски факултет, Ниш 2013, 95–105.",
"Бре. В." : "Вера Брежанчић, Орнитофаунистички резерват Хутово блато у светлу међународних конвенција, Природа Војводине, бр. XII–XIV, Покрајински завод за заштиту природе, Нови Сад година?, 129–136.",
"Бру. С." : "Спиридон Брусина, Орнитолошке биљешке за хрватску фауну, Гласник Хрватскога наравословнога друштва, година III, бр. 1, Загреб 1888, 129–150.",
"Бује" : "Ami Boué, La Turquie d'Europe, tome premier, Arthus Bertrand, Paris 1840.",
 "Вас. В. I" : "Војислав Васић – Георг Џукић, Орнитолошки рад грофа Алојзија Фердинанда Марсилија (1658–1730), Зборник за природне науке, бр. 53, Матица српска, Нови Сад 1977, 233–253.",
 "Вас. В. II" : "В. Ф. Васић – Ј. Шоти, Преглед фауна птица Власинског језера и околине, Биосистематика, вол. 6, бр. 1, Унија биолошких научних друштава Југославије, Земун 1980, 81–107..",
 "Вес. Д. I" : "Драгутин Весели, Прољетна сеоба птица по Босни и Херцеговини год. 1898, Ловачки лист, бр. 4, Савез ловачких удружења на подручју Босне и Херцеговине, Сарајево 1940, 195–197.",
 "Вес. Д. II" : "Драгутин Весели, Прољетна сеоба птица по Босни и Херцеговини год. 1898 (свршетак), Ловачки лист, бр. 6, Савез ловачких удружења на подручју Босне и Херцеговине, Сарајево 1940, 286–291.",
 "Вес. Д. III" : "Драгутин Весели, Јесења сеоба птица по Босни и Херцеговини год. 1897, Ловачки лист, бр. 9, Савез ловачких удружења на подручју Босне и Херцеговине, Сарајево 1940, 424–430.",
 "Вес. Д. IV" : "Драгутин Весели, Сеоба птица кроз Босну и Херцеговину, Ловачки лист, бр. 6, Савез ловачких удружења Народне Републике Босне и Херцеговине, Сарајево 1948, 155–157.",
 "Вес. Д. V" : "Драгутин Весели, Сове, Ловачки лист, бр. 1–2, Савез ловачких удружења Народне Републике Босне и Херцеговине, Сарајево 1949, 1–8.",
 "ВИЕЛ" : "Велика илустрована енциклопедија ловства, Грађевинска књига – Дневник, Београд – Нови Сад, I 1991, II 1992.",
 "Виз. О." : "Ондреј Визи, Заштићене животињске врсте у Црној Гори, Гласник Републичког завода за заштиту природе и Природњачког музеја у Титограду, 17, Титоград 1984, 69–108.",
 "ВЛ" : "Владалачки ловови (свршетак), Ловац, бр. 11–12, Савез ловачких удружења, Београд 1900, 161–166.",
 "Вод. М." : "Мато Водопић, Попис пучкијех птичијих имена, Словинац, бр. 2, књ. III, Дубровник 1880, 30–33.",
 "Вуј. Ј." : "Јоаким Вујић, Јестествословије, превод с немачког, Будим 1809.",
 "Вук" : "Вук Стефановић Караџић, Српски рјечник, 4. издање, Штампарија Краљевине Југославије, Београд 1935.",
 "Вук. Ж." : "Живко Вукасовић, Наравописје. За порабу гимназијалних учионицах у Хрватској и Славонији, Загреб 1850.",
 "Гар. Б. I" : "Борис Гаровников, Зимски гости наших ловишта, Ловачке новине, бр. 1–2, Дневник, Нови Сад 1982, 18–20.",
 "Гар. Б. II" : "Борис Гаровников – Милош Беуковић – Миленко Зеремски, Птице (перната дивљач) Дунавске бановине, Ловачки савез Војводине, Нови Сад 2008.",
 "Гар. Б. III" : "Борис Гаровников – Милош Беуковић – Миленко Зеремски, Које су то птице, Ловачки савез Војводине, Нови Сад 2009.",
 "Гар. Б. IV" : "Миленко Зеремски – Борис Гаровников, Вишејезични именик пернате дивљачи, Ловачки савез Војводине, Нови Сад 2010.",
 "Гаш. Б." : "Бранислав Гашић, Птице Републике Српске, Музеј Републике Српске, Бања Лука 1999.",
 "ГБК" : "Драгољуб Петровић, Говор Баније и Кордуна, Матица српска – Просвјета, Нови Сад – Загреб 1978.",
 "ГС" : "Момчило Поповић – Драгољуб Петровић, О говору Спича: Грађа, Српски дијалектолошки зборник, књ. LVI, САНУ – Институт за српски језик САНУ, Београд 2009, 1–275.",
 "ГСРПП I и II" : "Велимир Михајловић, Грађа за речник страних речи у предвуковском периоду, I том (А–Љ), Институт за лингвистику у Новом Саду, Нови Сад 1972, II том (М–Ш), Нови Сад 1974.",
 "Дев. М." : "Милан Девић, Црна гуска – редак гост наше фауне, Ловачке новине, бр. 14, Дневник, Нови Сад 1980, 9.",
 "Дел. В. I" : "Велид Делић, Запажања о сеоби птица, Ловачки лист, бр. 6, Савез ловачких удружења Народне Републике Босне и Херцеговине, Сарајево 1957, 364–370.",
 "Дел. В. II" : "Велид Делић, О сеоби птица, Ловачки лист, бр. 6, Савез ловачких удружења Народне Републике Босне и Херцеговине, Сарајево 1958, 327–334.",
 "Десп. П." : "Август Либен, Природопис, први део: Зоологија (превео П. Деспотовић), Панчево 1874.",
 "Док. Л." : "Лазар Ђ. Докић, Аналитички и систематски преглед животиња у Краљевини Србији, I део, Кичмењаци, Краљевско-српска државна штампарија, Београд 1883.",
 "Домбр. Е." : "Ернест Домбровски, Основи орнитологије сјеверозападне Србије, Гласник земаљског музеја у Босни и Херцеговини, књ. VII, Сарајево 1895, 63–104.",
 "Дусл Ј." : "Јосиф Дусл, Зоологија за средње школе, Београд 1870.",
 "Ђур. С. I" : "Стјепан Ђурашин, Птице, књ. XXIV, дио први, Матица хрватска, Загреб 1899.",
 "Ђур. С. II" : "Стјепан Ђурашин, Птице, књ. XXVI, дио други, Матица хрватска, Загреб 1901.",
 "Еле. Г. I" : "Гл. Елезовић, Соколари и соколарство, Стара Србија, Скопље 1923.",
 "Еле. Г. II" : "Глигорије Глиша Елезовић, Речник косовско-метохиског дијалекта, Графички уметнички завод „Планета”, Београд, свеска прва 1932, свеска друга 1935.",
 "Ети. Ј." : "Јосип Етингер, Сријемско-славонско-хрватске дивје животиње, звијери и птице, Тискарница Игњата Карла Сопрона, Земун 1857.",
 "Запл. Р." : "Рудолф Заплата, Птице уловљене у Сарајеву и околини од 1880–1940. године, Ловачки лист, Савез ловачких удружења на подручју Босне и Херцеговине, Сарајево 1940, бр. 3, 141–143, бр. 4, 192–194, бр. 5, 232–234, бр. 6, 278–280, бр. 7, 333–335, бр. 8, 386–388, бр. 10, 474–477, бр. 11, 534–537, 1941, бр. 2, 84–86, бр. 3, 134–136.",
 "ЗБГ" : "Збирка Бранислава Гашића.",
 "ЗНД" : "Збирка Ненада Дучића.",
 "ЗППС" : "Слободан Пузовић – Горан Секулић – Никола Стојнић – Братислав Грубач – Марко Туцаков, Значајна подручја за птице у Србији, Министарство животне средине и просторног планирања – Завод за заштиту природе Србије – Покрајински секретаријат за заштиту животне средине и одрживи развој, Београд 2009.",
 "ЗТН" : "Зоолошка терминологија и номенклатура. Средњошколска терминологија и номенклатура, књ. II, св. 2, Министарство просвете Краљевине Југославије, Београд 1932.",
 "Ива. Б." : "Божина Ивановић, Нека орнитолошка запажања на Скадарском језеру, Lаrus, вол. 21–22, годишњак Завода за Орнитологију ЈАЗУ, Загреб година? 1970 (24) (1967-68 21-22?), 137–160.",
 "Јед." : "Ф. Берж (F. Berge), Цивилизација животиња (превео Св. Попадић), Јединство, бр. 147, Београд 5. јул 1873, 294.",
 "Јов. В." : "Војкан Јовановић, Гуске, Зов, бр. 20, Борба, Београд 1984, 12–13.",
 "Кад. Х." : "Hans von Kadich, Hundert Tage im Hinterland (Eine ornithologische Forschungsreise in der Hercegowina), Mittheilungen des Ornithologischen Vereins in Wien, Wien 1887, 6–14, 23–25, 39–41, 61–63, 71–72, 85–86, 102–105, 121–123, 139–140, 154–157.",
 "Кап. М." : "Мехмедалија Капетановић, Птице рибњака Саничани, Природа, бр. 6, Загреб 1970, 176–177.",
 "Кла. В. I" : "Вјекослав Клаић, Природни земљопис Хрватске, књ. I, Матица хрватска, Загреб 1878.",
 "Кла. В. II" : "Вјекослав Клаић, Босна (земљопис), књ. III, Матица хрватска, Загреб 1878.",
 "Кне. М." : "Милан Кнежевић, Државно резервисано ловиште у Босни и Херцеговини, Ловачко-рибарски вјесник, бр. 2, Хрватско друштво за гојење лова и рибарства, Загреб 1933, 35–47..",
 "Кне. Р." : "Ратко Кнежевић, О тамањењу штетне дивљачи у ловиштима НР Босне и Херцеговине, Ловачки лист, бр. 6, Савез ловачких друштава Народне Републике Босне и Херцеговине, Сарајево 1953, 321–358.",
 "Кос. В." : "Валтазар Косић, Грађа за дубровачку номенклатуру и фауну птица, Гласник Хрватскога наравословнога друштва, година III, бр. 1, Загреб 1888, 118–128.",
 "Лаз. Г." : "Григорије Лазић, Проста наравна историја, Будим 1836.",
 "ЛВ" : "Рада Стијовић, Из лексике Васојевића, Српски дијалектолошки зборник, XXXVI, САНУ, Београд 1990.",
 "ЛЗЛФ" : "Вукоман Шелмић – Драган Гачић, Ловство са заштитом ловне фауне, Шумарски факултет, Београд 2011.",
 "Линт. Д." : "Lintia Dénes, Adatok Szerbia madárfaunájához (први део), Aquila (A magyar királyi ornithologiai központ folyóirata), XXII évfolyam, Budapest 1915, 329‒351. и Adatok Szerbia madárfaunájához (други део), Aquila (A magyar királyi ornithologiai központ folyóirata), XXIII évfolyam, Budapest 1916, 74‒162.",
 "ЛК" : "Драгољуб Петровић ‒ Јелена Капустина, Из лексике Качера. ‒ Српски дијалектолошки зборник, LVIII, САНУ, Београд 2011.",
 "Лов." : "Зоран А. Ристић, Ловство, Астон, Крагујевац 2008.",
 "ЛР" : "Драгослав Манић Форски, Лужнички речник, Дом културе Бабушница, Бабушница 1997.",
 "Мар. В." : "Вук Маринковић, Јестествена повестница, Београд 1851.",
 "Марч. М. I" : "Милорад Марчетић, Дивље патке, Војвођански ловац, бр. 92–93, Нови Сад 1955, 93–94.",
 "Марч. М. II" : "Милорад Марчетић, Заштита птица на територији Војводине, Заштита природе, бр. 7, Београд 1956, 5–11.",
 "Марч. М. III" : "Милорад Марчетић, Дивље гуске у фауни птица Војводине, Војвођански ловац, бр. 9–10, Нови Сад 1956, 155.",
 "Марч. М. IV" : "Милорад Марчетић, Сове Strigidae, Зборник за природне науке, бр. 11, Матица српска, Нови Сад 1956, 167–178.",
 "Марч. М. V" : "Милорад Марчетић, Орнитофауна Лудошког језера, Палићког језера и околине, Зборник за природне науке, бр. 11, Матица српска, Нови Сад 1956, 179–183.",
 "Марч. М. VI" : "Милорад Марчетић, Дивље патке у слици и речи, Војвођански ловац, бр. 11–12, Нови Сад 1958, 202–203.",
 "Марч. М. VII" : "Милорад Марчетић, Дивље гуске у нашим крајевима, Војвођански ловац, бр. 11–12, Нови Сад 1958, 204–205.",
 "Марч. М. VIII" : "Милорад Марчетић, Наши ретки гости – лабудови, Војвођански ловац, бр. 1–2, Нови Сад 1959, 12–13.",
 "Марч. М. IX" : "Милорад Марчетић – Душан Н. Андрејевић, Орнитофауна Косова и Метохије, Рилиндја, Приштина 1960.",
 "Матв. С. I" : "Сергије Д. Матвејев, Српска имена птица, Архив билошких наука, бр. 2, Институт за екологију и биогeографију Српске академије наука, Београд 1950, 146–158.",
 "Матв. С. II" : "Сергије Д. Матвејев, Распрострањење и живот птица у Србији, Посебна издања САНУ, књ. CLXI, Институт за екологију и биогеографију, књ. 3, Београд 1950.",
 "Матв. С. III" : "Сергије Д. Матвејев, Преглед фауне птица Балканског полуострва, I део, Детлићи и птице певачице, Посебна издања САНУ, књ. CDXCI, Одељење природно-математичких наука, књ. 46, Београд 1976.",
 "Мат. С. I" : "Свет. К. Матић, Орнитолошка збирка у нишкој гимназији, Извештај гимназије, Ниш 1905, 28–32.",
 "Мат. С. II" : "Свет. К. Матић, Птице у околини Ниша, Извештај гимназије, Ниш 1906, 48–53.",
 "Мед. М. I" : "Мојо Медић, Принос народној терминологији биљака и животиња, Летопис Матице српске, књ. 139, свеска трећа, Матица српска, Нови Сад 1884, 85–100.",
 "Мед. М. II" : "Мојо Медић, Додатак природописној и медицинској номенклатури, Летопис Матице српске, књ. 159, свеска трећа, Матица српска, Нови Сад 1889, 123–135.",
 "Мед. М. III" : "Мојо Медић, Додатак природописној и медицинској номенклатури (свршетак), Летопис Матице српске, књ. 160, свеска четврта, Матица српска, Нови Сад 1889, 70–91.",
 "Мед. М. IV" : "Мојо Медић, Грађа за природописну номенклатуру и за рибарско оруђе, Летопис Матице српске, књ. 166, свеска друга, Матица српска, Нови Сад 1889, 60–81.",
 "Мед. М. V" : "Мојо Медић, Други додатак грађи за природописну номенклатуру и за рибарско оруђе, Летопис Матице српске, књ. 184, свеска четврта, Матица српска, Нови Сад 1895, 13–27.",
 "Мед. М. VI" : "Мојо Медић, Други додатак грађи за природописну номенклатуру и за рибарско оруђе (свршетак), Летопис Матице српске, књ. 188, свеска четврта, Матица српска, Нови Сад 1895, 120–134.",
 "Мед. М. VII" : "Мојо Медић, Зоологија за више разреде средњих школа, Краљевска хрватско-славонска земаљска влада, Загреб 1920.",
 "Мил. П." : "Пера Милић, Орнитолошке занимљивости из околине Новог Сада, Војвођански ловац, бр. 3–6, Нови Сад 1959, 72–74.",
 "НГ" : "Милорад Марчетић, Наше грабљивице, Војвођански ловац, Савез ловачких друштава Војводине, Нови Сад 1953, бр. 72–73, 32–34, бр. 72–75, 34–36, 1954, бр. 76–77, 22–23.",
 "НИПБХ" : "Отмар Рајзер ‒ Иван Сеуник, Народна имена птица у Босни и Херцеговини, Гласник земаљског музеја у Босни и Херцеговини, књ. I, Сарајево 1890, 109‒112.",
 "НПВ" : "Рихард Чорнаи, Номенклатура птица Војводине (од бр. 25–26 Номенклатура птица у Војводини), Војвођански ловац, Савез ловачких друштава Војводине, Нови Сад 1947, бр. 16, 215–216, бр. 17, 233–234, бр. 18–19, 259–260, 1948, бр. 21–22, 296–297, бр. 23–24, 330, бр. 25–26, 355–356, бр. 27–28, 381–382, бр. 29–30, 407–408, бр. 31, 428–429, 1949, бр. 32–34, 453–454, бр. 35–37, 487–489, бр. 38–41, 513–514, бр. 42–43, 543–545, 1950, бр. 47–49, 593–594, 1952, бр. 56–57, 16–17, бр. 58–59, 13–14, бр. 61, 14–15, бр. 62–63, 23–24, 1953, бр. 64–65, 23–24, бр. 66–67, 20–21, бр. 68–69, 24–25, бр. 70–71, 17–18.",
 "Орф. З." : "Захарија Орфелин, Мелодија к пролећу, Нови Сад 1765.",
 "Ост. А." : "А. Остојић, Прилог за народну номенклатуру, Гласник Хрватскога наравословнога друштва, година II, бр. 1, Загреб 1887, 119–129.",
 "ОЦБ" : "Борис Гаровников – Естер Поповић, Орнитофауна Царске баре, Природа Војводине, IX–XI, Покрајински завод за заштиту природе, Нови Сад 1986, 39–54.",
 "Панч. Ј. I" : "Јосиф Панчић, Јестаственица (за ученике велике школе), део 1, Зоологија, Државна штампарија, Београд 1864.",
 "Панч. Ј. II" : "Јосиф Панчић, Птице у Србији, Државна штампарија, Београд 1867.",
 "ПАп" : "Јован Лакатош, Птице Апатина, Глас комуне, Апатин 1979.",
 "ПБан" : "Јавор Рашајски – Андреи Киш (Andrei Kiss), Птице Баната, Градски музеј Вршац, Вршац 2004.",
 "ПБар" : "Бранислав Гашић – Горан Дујаковић, Птице Бардаче, Републички завод за заштиту културно-историјског и природног насљеђа Републике Српске, Бања Лука 2009.",
"ПБС" : "Растко Александров, Птице Божја створења, Штампарија Српске патријаршије, Београд 1993.",
"ПВП" : "Јавор Рашајски – Иштван Пеле (Istvan Pelle), Птице Вршачких планина, Матица српска, Нови Сад 1993.",
"ПГБач" : "Радивој Обрадовић, Птице грабљивице Бачке, Еколошко друштво Апатин, Апатин 1994.",
"ПДКТ" : "Војислав Васић – Саша Маринковић – Ондреј Визи, Птице Дурмитора и кањона Таре, Фауна Дурмитора, св. 3, ЦАНУ, Титоград 1990, 9–70.",
"ПДП" : "Михаило Вучковић – Ондреј Визи, Прилог проучавању орнитофауне Црне Горе (птице долине Пиве), Глас. Републичког завода зашт. природе – Природњачког музеја, 10, Титоград 1977, 41–58.",
"Пек. Б." : "Божидар Пекић, Прилог познавању орнитофауне Царске Баре са околином, Заштита природе, бр. 14, Београд 1958, 11–19.",
"Петр. Б." : "Борис Петров, Орнитофенолошки извештај из околине Прокупља, прештампано из Ловца, бр. 1–2, Савез ловачких удружења, Београд 1941.",
"Петр. Ј." : "Јован Петровић, Наука о животињама, Платонова штампарија, Нови Сад 1867.",
"Пец. Ј." : "Јосиф Пецић, Наука о животињама, Краљевско-српска државна штампарија, Београд 1884.",
"ПЗас" : "Димитрије Радишић – Марко Шћибан – Милан Ружић – Михајло Станковић, Птице Засавице, Покрет горана Сремске Митровице, Сремска Митровица 2010.",
"ПЈуг 1" : "В. Е. Мартино – С. Д. Матвејев, Птице Југославије, I, Скупљање, препарирање и одређивање, Просвета, Београд 1947.",
"ПЈуг 2" : "Радивој Обрадовић, Птице Југославије, Сомбор 1998.",
"ПКоп" : "Сергије Д. Матвејев, Птице Копаоника, Завод за заштиту природе Србије – Јавно предузеће „Национални парк Копаоник”, Београд 1997.",
"ПЛик" : "Радивој Обрадовић, Птице Лике, Еколошко друштво Горње Подунавље – Гимназија Никола Тесла, Апатин 1995.",
"ПОВ I и II" : "Велимир Михајловић, Посрбице од Орфелина до Вука, I том (Б–О), Матица српска, Нови Сад 1982, II том (П–Ш), Нови Сад 1984.",
"Понг. Р. В." : "Р. В. Понграц, Стрвинари пред објективом, Ловачки гласник, бр. 9–10, Савез ловачких удружења за Дунавску бановину, Нови Сад 1936, 258–262.",
"Поп. Ј." : "Јелена Поповић, Еколошка инвентаризација орнитофауне у кањону реке Увац, сепарат, Зборник радова Републичког завода за заштиту природе СР Србије, књ. 2, бр. 4, Београд 1974.",
"ПСВВ" : "Јосиф Валдхер, Фауна. ‒ Повесница слободне краљеве вароши Вршца, Панчево 1886, 234‒239.",
"ПСрб" : "Јавор Рашајски, Птице Србије, Triton Public, Вршац 2004.",
"ПХС I" : "Спиро Брусина, Птице хрватско-српске, Споменик, I, Српска краљевска академија, Београд 1888.",
"ПХС II" : "Спиро Брусина, Птице хрватско-српске, Споменик, XII, Српска краљевска академија, Београд 1892.",
"Рајз. О. I" : "Отмар Рајзер, Пребивања четирију врста европских лешинара у Босни и Херцеговини, Гласник земаљског музеја у Босни и Херцеговини, књ. I, Сарајево 1889, 51–57.",
"Рајз. О. II" : "Отмар Рајзер, Гдје у Босни и Херцеговини има дојако опажаних врста из рода патака (Anatidae) и куда се шире, Гласник земаљског музеја у Босни и Херцеговини, књ. IV, Сарајево 1889, 119–125.",
"Рајз. О. III" : "Отмар Рајзер, Додатак к списку птица у Босни и Херцеговини, Гласник земаљског музеја у Босни и Херцеговини, књ. II, Сарајево 1891, 262–263.",
"Рајз. О. IV" : "Oтмар Рајзер – Иван Кнотек, Резултати посматрања сеобе птица по Босни и Херцеговини, Гласник земаљског музеја у Босни и Херцеговини, књ. XII, Сарајево 1900, 275–411.",
"Рајз. О. V" : "Отмар Рајзер, Извјештај о успјеху орнитолошких путовања у Србији године 1899. и 1900, Гласник земаљског музеја у Босни и Херцеговини, књ. XVI, Сарајево 1904, 125–152.",
"Рашк. М. Н. I" : "М. Н. Рашковић, Један прилог за упознавање тичијег света у Врањском округу, Ловац, бр. 8, Савез ловачких удружења, Београд 1897, 59.",
"Рашк. М. Н. II" : "М. Н. Рашковић, Један прилог за упознавање тичијег света у Врањском округу (наставак), Ловац, бр. 9, Савез ловачких удружења, Београд 1897, 66.",
"Рашк. М. Н. III" : "М. Н. Рашковић, Један прилог за упознавање тичијег света у Врањском округу (наставак), Ловац, бр. 12, Савез ловачких удружења, Београд 1897, 90–91.",
"Рашк. М. Н. IV" : "Михаило Н. Рашковић, Дропљица, Ловац, бр. 3 и 4, Савез ловачких удружења, Београд 1898, 18–19.",
"Рашк. М. Н. V" : "Михаило Н. Рашковић, О тичијем свету у Крајини, Први конгрес српских лекара и природњака, Београд 1905.",
"РГЗ" : "Драго Ћупић ‒ Жељко Ћупић, Речник говора Загарача. ‒ Српски дијалектолошки зборник, XLIV, САНУ, Београд 1997.",
"РГЈК" : "Радмила Жугић, Речник говора јабланичког краја, Српски дијалектолошки зборник, LII, САНУ, Београд 2005.",
"РДГ" : "Михаило Бојанић ‒ Растислава Тривунац, Рјечник дубровачког говора, Српски дијалектолошки зборник, XLIX, САНУ, Београд 2002.",
"РЈС" : "Момчило Златановић, Речник говора јужне Србије, Врањске књиге, Врање 2008.",
"РК" : "Драгољуб Петровић – Ивана Ћелић – Јелена Капустина, Речник Куча, Српски дијалектолошки зборник, LX, САНУ – Институт за српски језик САНУ, Београд 2013.",
"РЛГ" : "Бранислав Митровић, Речник лесковачког говора, Ленекс, Београд 1992.",
"РМС" : "Речник српскохрватскога књижевног језика, књ. 1–6, Матица српска, Нови Сад 1967–1976.",
"РНГЦР I" : "Миодраг Марковић, Речник народног говора у Црној Реци. – Српски дијалектолошки зборник, XXXII, САНУ, Београд 1986.",
"РНГЦР II" : "Миодраг Марковић, Речник народног говора у Црној Реци. – Српски дијалектолошки зборник, XXXIX, САНУ, Београд 1993.",
"РСГВ" : "Речник српских говора Војводине, св. 1–10, Матица српска, Нови Сад 2000–2010.",
"РПГ-Ж" : "Новица Живковић, Речник пиротског говора, Музеј Понишавља, Пирот 1987.",
"РПГ-З" : "Драгољуб Златковић, Речник пиротског говора, Службени гласник, Београд 2014.",
"РСАНУ" : "Речник српскохрватског књижевног и народног језика, књ. I–XIX, Институт за српскохрватски језик САН / Институт за српски језик САНУ, Београд 1959–2014.",
"РСК I" : "Властимир Јовановић, Речник села Каменице код Ниша, Српски дијалектолошки зборник, књ. LI, САНУ – Институт за српски језик САНУ, Београд 2004, 313–688.",
"РСК II" : "Властимир Јовановић, Додатак Речнику села Каменице код Ниша, Српски дијалектолошки зборник, књ. LIV, САНУ – Институт за српски језик САНУ, Београд 2007, 403–520.",
"РСН" : "Ђорђе Поповић, Речник српскога и немачкога језика, II српско-немачки део, непромењено друго прегледано и умножено издање, књижара „Напредак” из Панчева, Београд 1926.",
"Руцн. Д." : "Драгутин Руцнер, Прилог познавању народне номенклатуре птица с подручја Конавала (Далмација), Larus, вол. 21–22, годишњак Завода за Орнитологију ЈАЗУ, Загреб 1970, 195–196.",
"Себ. Ђ. I" : "Ђуро Себишановић, Грађа за номенклатуру наших птица, Гласник Хрватскога наравословнога друштва, година IV, бр. 1, Загреб 1889, 261–272.",
"Себ. Ђ. II" : "Ђуро Себишановић, Орнитолошка вијест из вараждинског краја за годину 1889, Гласник Хрватскога наравословнога друштва, година IV, бр. 1, Загреб 1889, 312–315.",
"Сев. А." : "Александар Северјанин, Северни гости, Ловац, бр. 3–4, Савез ловачких удружења, Београд 1930, 58–60.",
"Сим. Д. Т." : "Драгутин Т. Симоновић, Птице, I, Грабљивице, пузачице, викачице, издање Задруге професорског друштва, Београд 1939. и друго издање, Знање, Београд 1953.",
"Скок" : "Петар Скок, Етимологијски рјечник хрватскога или српскога језика, I–IV,  ЈАЗУ, Загреб 1971–1974.",
"СН" : "В. Ф. Васић – Д. В. Симић – Ж. Станимировић – М. Каракашевић – М. Шћибан – М. Ружић – С. Кулић – М. Кулић – С. Пузовић, Српска номенклатура I, Двоглед, бр. 4, Лига за орнитолошку акцију Србије и Црне Горе, Београд 2004, 7–19 и Српска номенклатура II, Двоглед, бр. 5, Лига за орнитолошку акцију Србије и Црне Горе Београд 2005, 10–18.",
"ССМ" : "Грађа за фауну Старе Србије и Маћедоније, прештампано из часописа Просветни гласник, Музеј Српске земље, посебно издање 6, Државна штампарија Краљевине Србије, Београд 1907.",
"Стан. Ј." : "Ј. Стантић, На македонским водама, Ловац, бр. 5, Савез ловачких удружења, Београд 1950, 7–12.",
"Сто. А." : "Атанасије Стојковић, Физика, Будим 1803.",
"Сто. Д." : "Душан Стојићевић, Научна имена српско-хрватских птица, сепаратни отисак из Југословенске шуме, бр. 2, Музеј Српске земље, Београд 1938.",
"Суп" : "Саша Маринковић – Бранко Караџић, Суп, Библиотека Фонд за заштиту птица грабљивица, књ. I, Институт за билошка истраживања „Синиша Станковић”, Београд 2008.",
"ТДР" : "Јакша Динић, Тимочки дијалекатски речник, Институт за српски језик САНУ, Београд 2008.",
"Трст. Д. I" : "Животиње, V део, Даворин Трстењак, Птице, I свезак, књ. LXIX, Друштво Св. Јеронима, Загреб 1888.",
"Трст. Д. II" : "Животиње, VI део, Даворин Трстењак, Птице, II свезак, књ. LXXVII, Друштво Св. Јеронима, Загреб 1890.",
"Трст. Д. III" : "Животиње, VII део, Даворин Трстењак, Птице, III свезак, књ. LXXXX, Друштво Св. Јеронима, Загреб 1893.",
"Трст. Д. IV" : "Животиње, VIII део, Даворин Трстењак, Птице, IV свезак, књ. XCVII, Друштво Св. Јеронима, Загреб 1895.",
"ФЗЦГ" : "Вукић Пулевић – Новица Самарџић, Фитоними и зооними у топонимији Црне Горе, ДАНУ, Подгорица 2003.",
"Финк" : "Алфред Едмунд Брем, Како живе животиње (по оригиналном пучком издању приредио с особитим обзиром на наш животињски свијет проф. др Никола Финк), Минерва, Загреб 1937.",
"Фир. Љ. I" : "Људевит Фирер, Једна година орнитолошког изучавања у Црној Гори, Гласник земаљског музеја у Босни и Херцеговини, књ. VI, Сарајево 1894, 543–608.",
"Фир. Љ. II" : "Људевит Фирер, Продужена посматрања на орнитолошком пољу у Црној Гори, Гласник земаљског музеја у Босни и Херцеговини, књ. VII, Сарајево 1895, 241–258.",
"ФЈ" : "Сергије Д. Матвејев, Фауна Југославије, сепарат, Енциклопедија Југославије, св. IV, Лексикографски завод ФНРЈ, Загреб 1960.",
"Фрач. М." : "Миша Т. Фрачковић, Јестаственица за школу и домаћу наставу (по Гертнеру), Књижара браће Јовановића, Панчево 1874.",
"Хирц Д." : "Драгутин Хирц, Грађа за народну номенклатуру и терминологију животиња (III, Птице), Наставни вјесник, часопис за средње школе, књ. VII, Краљевска хрватско-славонско-далматинска земаљска влада, Загреб 1899, 145–155.",
"Хирц М." : "Мирослав Хирц, Рјечник народних зоологичких назива, књига друга: Птице (Aves), ЈАЗУ, Загреб 1938–1947.",
"ЦЛПВ" : "Борис Гаровников – Иштван Хам, Прва „црвена листа” птица Војводине, Природа Војводине, VI–VII, Покрајински завод за заштиту природе, Нови Сад 1980–1981, 59–63. и Борис Гаровников – Иштван Хам, Прва „црвена листа” птица Војводине (прве допуне и корекције), Природа Војводине, IX–XI, Покрајински завод за заштиту природе, Нови Сад 1986, 59–63.",
"ЦР" : "Радосав Стојановић, Црнотравски речник, Српски дијалектолошки зборник, књ. LVII, САНУ – Институт за српски језик САНУ, Београд 2010.",
"Црн. К." : "Коста Црногорац, Природна историја, део 1, Зоологија, Државна штампарија, Београд 1870.",
"Чор. Р." : "Csornai Rihárd, Bácska madarainak szerb és horvátnyelvü névjegyzéke, Aquila (A magyar királyi Madártani Intézet folyóirata), L évfolyam, Budapest 1943, 394–402.",
"Џај. А." : "Анто Џаја, Ружевац нестао заувек, Зов, бр. 15, Борба, Београд 1984, 10.",
"Шев. А." : "Александар Шевић, Извештај о раду, Војвођански ловац, бр. 23–24, Нови Сад 1948, 311–323."}

class Entry():
    def __init__(self, name):
        self.name = name
        self.synonyms = []
        
class Latin_genus(Entry):
    def __init__(self, name):
        self.hyponyms = []
        
class Serbian_genus(Entry):
    def __init__(self, name):
        self.latin_names = None
        self.hyponyms = []
    
class Latin_species(Entry):
    def __init__(self, name):
        srb_genus = None
        lat_genus = None
        self.hyperonyms = []
        
class Serbian_species(Entry):
    def __init__(self, name):
        srb_genus = None
        lat_genus = None
        self.hyperonyms = []

def find_duplicate_keys(d, no_of_dup):
    """
    Read dictionary keys and figure out which are duplicates. Store them in a
    txt file. If the file exists it skips this step and reads the file.
    """
    if os.path.isfile("duplicates.txt"):
        duplicates = open("duplicates.txt", "r", encoding="utf8").read().split()
        return duplicates
    else:
        all_keys = d.keys()
        all_keys_list = [re.sub(r'\{[^}]*\}', '', x).strip() for x in all_keys]
        ordered_keys = Counter(all_keys_list).most_common(no_of_dup)
        duplicates = ([x[0] for x in ordered_keys if x[1] > 1])
        outfile = open("out/duplicates.txt", "w", encoding="utf8")
        outfile.write("\n".join(duplicates))
        return duplicates
    
def get_type_of_entry(dictionary, s, entry):
    """
    Transfering entries from parsing class to wiki class.
    """
    return entry
    
def concat_entry(string):
    return string
    
def format_latin_species(species):
    return species
    
def format_serbian_species(species):
    return species

def expand_dictionary(dictionary):
    dict_of_wiki_entries = {}
    for k in dictionary:
        all_srb_spec = {}
        all_lat_spec = {}
        genus = k
        genus_lat_name = ' '.join([k, dictionary[k][k]['latin name'], dictionary[k][k]['discoverer']])
#        print(genus_lat_name)
        genus_serbian_name = dictionary[k][k]['serbian name'] #+ ' <ref' + dictionary[k][k]['latin name'][1] + '/ref>'
        for i, spec in enumerate(dictionary[k][k]['species']):
            latin_species = dictionary[k][k]['species'][spec][1]
            latin_species = format_latin_species(latin_species)
            all_lat_spec[i] = latin_species
            serbian_species = dictionary[k][k]['species'][spec][2]
            serbian_species = format_serbian_species(serbian_species)
            all_srb_spec[i] = serbian_species
            
        lat_gen_entry = Latin_genus(genus_lat_name)
        lat_gen_entry.hyponyms = all_lat_spec
        for srb_spec in genus_serbian_name:
            srb_gen_entry = Serbian_genus(srb_spec[0])
            srb_genus_synonym = [x for x in genus_serbian_name if x[0] != srb_spec[0]]
            srb_gen_entry.synonyms = srb_genus_synonym
            srb_gen_entry.hyponyms = all_srb_spec
            srb_gen_entry.latin_names = genus_lat_name
        
    return dict_of_wiki_entries
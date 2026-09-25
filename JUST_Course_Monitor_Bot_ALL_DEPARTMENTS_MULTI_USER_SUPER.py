import time
import json
import re
import random
import os
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from patchright.sync_api import sync_playwright


TELEGRAM_TOKEN = "8849536857:AAHpnQSUhNkMZKCC6UzctQ7RibuitJaHqqc"

PROFILE_FOLDER = r"C:\Users\owndi\just_bot\browser_profile"

FACULTY_VALUE = "70"
INITIAL_DEPT_VALUE = "178"

DEPARTMENT_NAMES = {
    "82": "العلوم الأساسية الإنسانية والعلمية",
    "84": "علوم العسكرية",
    "173": "علوم الحاسوب",
    "174": "نظم المعلومات الحاسوبية",
    "178": "علم البيانات",
    "179": "الذكاء الاصطناعي",
    "203": "نظم المعلومات الصحية",
    "80": "عربي",
    "81": "اللغة الانجليزية واللغويات",
    "90": "الرياضيات",
    "176": "هندسة البرمجيات",
    "-1": "مركز اللغات"
}

DEPARTMENT_FACULTIES = {
    "82": "90",
    "84": "80",
    "173": "70",
    "174": "70",
    "178": "70",
    "179": "70",
    "203": "70",
    "80": "90",
    "81": "90",
    "90": "90",
    "176": "70",
    "-1": "122"
}

FACULTY_NAMES = {
    "70": "كلية تكنولوجيا المعلومات",
    "90": "العلوم والآداب",
    "80": "شعبة العلوم العسكرية",
    "122": "مركز اللغات"
}

COURSE_NAMES = {
    "821152": "مختبر البرمجة في علوم الذكاء الإصطناعي",
    "822214": "أساسيات قواعد البيانات",
    "1740990": "مهارات الحاسوب / استدراكي",
    "1742010": "مقدمة في تصميم صفحات الوب",
    "1743410": "تطوير تطبيقات الوب",
    "1743910": "التدريب الميداني",
    "1744210": "تطبيقات قواعد البيانات",
    "1744410": "تراسل بيانات الأعمال",
    "1744910": "مشروع تخرج (1)",
    "1744920": "مشروع تخرج (2)",
    "1747010": "اساسيات علم البيانات",
    "1747100": "مقدمة إلى نظم المعلومات الصحية",
    "1747110": "الاحصاء لعلم البيانات",
    "1747120": "إدارة نظم الرعاية الصحية وضبط الجودة",
    "1747220": "تحليل البيانات",
    "1747230": "معالجة البيانات الصحية",
    "1747450": "امن البيانات",
    "1747810": "ندوه في علم البيانات",
    "1747990": "رسالة الماجستير",
    "1747991": "رسالة الماجستير",
    "1747992": "رسالة الماجستير",
    "1747993": "رسالة الماجستير",
    "1792440": "برمجة الذكاء الاصطناعي",
    "1792442": "برمجة الذكاء الاصطناعي",
    "1792450": "مختبر برمجة الذكاء الاصطناعي",
    "1792490": "تعلم الآلة",
    "1792491": "تعلم الآلة عملي",
    "1792750": "تصميم المنطق الرقمي وتنظيم الحاسوب",
    "1793280": "معالجة البيانات الكبيرة",
    "1793420": "التعلم العميق",
    "1793750": "معالجة الصور الرقمية",
    "1793800": "خوارزميات التحسين",
    "1793810": "إدارة عمليات التعلم الآلي",
    "1794450": "معالجة اللغات الطبيعية",
    "1794470": "الرؤية الحاسوبية",
    "1794900": "التدريب الميداني",
    "1794910": "مشروع التخرج (1)",
    "1794920": "مشروع التخرج (2)",
    "821052": "السلامة المروية",
    "821104": "التربية الوطنية والمسؤولية المجتمعية",
    "821105": "التربية الوطنية والمسؤولية المجتمعية باللغة الانجليزية",
    "821106": "التربية الوطنية",
    "821192": "الريادة والإبتكار",
    "821200": "الريادة والإبتكار والمهارات الحياتية",
    "821300": "الثقافة الرقمية",
    "821411": "مبادئ في الاقتصاد (غير طلبة نظم المعلومات الحاسوبية)",
    "821511": "مبادىء في العلوم الاداريه (غير طلبة نظم المعلومات الحاسوبية)",
    "821531": "الاسلام والتحديات المعاصرة",
    "822210": "مبادىء علم النفس (باللغة الانجليزية)",
    "822520": "الفكر العالمي (باللغة الإنجليزية)",
    "823020": "مبادئ علم الاجتماع لطلبة كلية التمريض",
    "841000": "العلوم العسكريه",
    "2032010": "مختبر تصميم صفحات الوب",
    "2033210": "تحليلات بيانات الرعاية الصحية",
    "2033211": "تحليلات بيانات الرعاية الصحية",
    "2033320": "تصور واكتشاف البيانات",
    "2033321": "تحليل وتصميم الأنظمة",
    "2033350": "تطوير التطبيقات الخلوية والتطبيب عن بعد",
    "2033910": "التدريب الميداني",
    "2034200": "تطبيقات الذكاء الاصطناعي في الرعاية الصحية",
    "2034910": "مشروع تخرج (1)",
    "2034911": "التدريب الميداني 2",
    "2034920": "مشروع تخرج (2)",
    "1781010": "أساسيات علوم البيانات",
    "1781011": "أساسيات علوم البيانات والذكاء الاصطناعي",
    "1781020": "مختبر أساسيات علوم البيانات",
    "1781101": "البرمجة في علوم البيانات",
    "1781110": "البرمجة في علوم البيانات (2)",
    "1781120": "مختبر البرمجة في علوم البيانات",
    "1782301": "تعلم الآلات",
    "1782320": "مختبر تعلم الآلات",
    "1783210": "البيانات الكبيرة",
    "1783300": "التعلم العميق",
    "1783600": "أمن المعلومات",
    "1783950": "التدريب الميداني",
    "1784221": "قواعد البيانات غير المهيكلة",
    "1784390": "حوكمة البيانات",
    "1784500": "معالجة اللغات الطبيعية",
    "1784510": "استرجاع المعلومات",
    "1784540": "ادارة المشاريع",
    "1784580": "تحليل الأعمال",
    "1784800": "مشروع تخرج (1)",
    "1784810": "مشروع تخرج (2)",
    "1784930": "مواضيع خاصة في علوم البيانات (3)",
    "821061": "مختبر البرمجة",
    "821151": "البرمجة بلغة سي++",
    "822112": "تراكيب البيانات",
    "822123": "مختبر تراكيب البيانات",
    "1732160": "مختبر نمذجة البرمجه كينونية التوجه",
    "1732841": "تحليل وتصميم الخوارزميات",
    "1733180": "تفاعل الإنسان والحاسوب",
    "1733620": "الذكاء الاصطناعي",
    "1733750": "مبادئ نظم التشغيل الحديثة",
    "1733850": "اساسيات الوسائط المتعددة",
    "1733910": "التدريب الميداني",
    "1734511": "معمارية الحاسوب",
    "1734820": "معالجة الصور",
    "1734910": "مشروع تخرج (1)",
    "1734911": "مشروع تخرج (1)",
    "1734920": "مشروع تخرج (2)",
    "1734921": "مشروع تخرج (2)",
    "1737100": "هندسة البرمجيات المتقدمة",
    "1737420": "شبكات الحاسوب المتقدمه",
    "1737620": "الذكاء الاصطناعي المتقدم",
    "1737750": "انظمة التشغيل المتقدمة",
    "1737830": "الابصار بالحاسوب المتقدمة",
    "1737891": "ندوه في علوم الحاسوب",
    "1737993": "رسالة الماجستير",
    "1737994": "رسالة الماجستير",
    "1737995": "رسالة الماجستير",
    "1737996": "رسالة الماجستير",
    "8210111": "مقدمة في البرمجة",
    # هندسة البرمجيات - 176
    "821125": 'مقدمة في البرمجة الكينونية',
    "821127": 'مقدمة في البرمجة الكينونية',
    "821131": 'مختبر البرمجة الكينونية',
    "1762100": 'البرمجة بلغة جافا',
    "1762110": 'مختبر البرمجة بلغة جافا',
    "1762200": 'نمذجة البرمجيات',
    "1762300": 'أساسيات هندسة البرمجيات',
    "1763100": 'البرمجة المرئية',
    "1763210": 'هندسة متطلبات البرمجيات',
    "1763231": 'توثيق البرمجيات',
    "1763240": 'معمارية و تصميم البرمجيات',
    "1763250": 'مختبر هندسة البرمجيات "2"',
    "1763710": 'برمجة الخادم/المستفيد',
    "1763900": 'التدريب الميداني',
    "1764120": 'لغة برمجة مختارة',
    "1764300": 'فحص البرمجيات',
    "1764310": 'امن البرمجيات',
    "1764320": 'هندسة تطبيقات الوب',
    "1764400": 'إدارة المشاريع',
    "1764911": 'مشروع تخرج "1"',
    "1764921": 'مشروع تخرج "2"',
    "1764950": 'موضوعات خاصة في هندسة البرمجيات "3"',
    "8210211": 'مهارات اللغة الإنجليزية في تكنولوجيا المعلومات',
    # الرياضيات - 90
    "821011": 'الرياضيات',
    "821021": 'حساب التفاضل والتكامل (1)',
    "821023": 'حساب التفاضل والتكامل (2)',
    "821034": 'رياضيات متقطعة',
    "821038": 'مبادئ الاحصاء والاحتمالات',
    "822010": 'تفاضل وتكامل (1)',
    "822030": 'تفاضل وتكامل (2)',
    "822212": 'الرياضيات المتقطعه',
    "822331": 'إحصاء واحتمالات لطلبة الحاسوب',
    "822350": 'احصاء واحتمالات',
    "822411": 'الرياضيات المتقطعه',
    "900990": 'رياضيات عامه - استدراكي -',
    "901111": 'مقدمة في الحاسوب',
    "901310": 'مبادىء الاحصاء',
    "901320": 'مبادىء في الاحصاء الحيوي',
    "901400": 'مبادىء الجبر الخطي',
    "901450": 'اسس الرياضيات',
    "902450": 'نظرية المجموعات والمنطق',
    "903011": 'تفاضل وتكامل متقدم',
    "903050": 'مقدمه في المعادلات التفاضليه الجزئيه',
    "903071": 'تحليل حقيقي (1)',
    "903212": 'التحليل العددي والاساليب الحسابية الذكية',
    "903300": 'احصاء رياضي',
    "903312": 'الاساليب الاحصائية وتفسير الذكاء الاصطناعي',
    "903391": 'تحليل السلاسل الزمنية',
    "903400": 'الجبر الخطي',
    "903420": 'الجبر التجريدي (1)',
    "903450": 'نظرية العدد',
    "903470": 'نظرية الرسوم',
    "903620": 'التوبولوجي (1)',
    "904070": 'تحليل حقيقي (2)',
    "904420": 'الجبر التجريدي (2)',
    "904921": 'بحث في الرياضيات التطبيقيه -لطلبة 97 فما بعد -',
    "904932": 'اساليب تدريس الرياضيات النظرية والتطبيق',
    "904970": 'موضوعات في التحليل',
    "904980": 'موضوعات في الجبر',
    "907010": 'طرق متقدمه في الرياضيات التطبيقيه',
    "907070": 'التحليل الحقيقي - 1 -',
    "907090": 'التحليل الحقيقي (2)',
    "907210": 'التحليل العددي (1)',
    "907310": 'نظرية الاحتمالات',
    "907410": 'الجبر المجرد (1)',
    "907910": 'ندوه',
    "907950": 'دراسات مستقله',
    "907996": 'رسالة الماجستير',
    "907997": 'رسالة ماجستير',
    "907998": 'رسالة الماجستير',
    "907999": 'رسالة الماجستير',
    # اللغة الانجليزية واللغويات - 81
    "812413": 'الأنماط الأدبية',
    "812712": 'الأشكال والوظيفية في اللغة الإنجليزية',
    "813050": 'تاريخ اللغة الانجليزية',
    "813070": 'المعجمية وأصول الكلمات',
    "813300": 'اللغة الإنجليزية كلغة أجنبية',
    "813512": 'علم الإشتقاق',
    "813600": 'علم الدلاله',
    "813610": 'السيميائية',
    "813722": 'القواعد الوظيفيه',
    "813920": 'أساليب البحث العلمي',
    "814031": 'علم اللغه النفسي',
    "814050": 'الاسلوبية',
    "814060": 'علم اللغه الاجتماعي',
    "814121": 'اللغويات العصبية',
    "814930": 'مواضيع خاصة',
    "817110": 'الاتصال عبر الثقافات',
    "817711": 'علم النحو',
    "817960": 'اللغويات العصبية',
    "817980": 'امتحان الشامل',
    "817994": 'رسالة الماجستير',
    "817996": 'رسالة الماجستير',
    "817997": 'رسالة الماجستير',
    "817999": 'رسالة الماجستير',
    "871010": 'اللغويات 1',
    "871710": 'القواعد والإنشاء',
    "872010": 'علم الأصوات',
    "2511111": 'الاستماع والمحادثة',
    # عربي - 80
    "801022": 'اللغة العربية ومهارات الإتصال والتواصل',
    "801023": 'اللغة العربية ومهارات الإتصال والتواصل (لغير الناطقين باللغة العربية)',
    "802000": 'تذوق النص الادبي',
    "802010": 'الأدب الأردني',
    "802020": 'علم اللغويات العربية (لطلبة قسم اللغة الإنجليزية واللغويات)',
    # مركز اللغات - -1
    "2510990": 'لغة انجليزية استدراكي',
    "2511010": 'اللغة الإنجليزية ومهارات الإتصال والتواصل',
    "2511030": 'المهارات الحياتية',
    "2511040": 'مهارات أساسية في اللغة الصينية',
    "2511050": 'مبادئ في اللغة الفرنسية',
    "2511080": 'اللغة التركية',
    "2515030": 'برنامج تأهيلي في اللغة الانجليزية لطلبة الدراسات العليا'
}

COURSE_DEPARTMENTS = {
    # علوم الحاسوب - 173
    "821061": "173",
    "821151": "173",
    "822112": "173",
    "822123": "173",
    "1732160": "173",
    "1732841": "173",
    "1733180": "173",
    "1733620": "173",
    "1733750": "173",
    "1733850": "173",
    "1733910": "173",
    "1734511": "173",
    "1734820": "173",
    "1734910": "173",
    "1734911": "173",
    "1734920": "173",
    "1734921": "173",
    "1737100": "173",
    "1737420": "173",
    "1737620": "173",
    "1737750": "173",
    "1737830": "173",
    "1737891": "173",
    "1737993": "173",
    "1737994": "173",
    "1737995": "173",
    "1737996": "173",
    "8210111": "173",

    # نظم المعلومات الحاسوبية - 174
    "821152": "174",
    "822214": "174",
    "1740990": "174",
    "1742010": "174",
    "1743410": "174",
    "1743910": "174",
    "1744210": "174",
    "1744410": "174",
    "1744910": "174",
    "1744920": "174",
    "1747010": "174",
    "1747100": "174",
    "1747110": "174",
    "1747120": "174",
    "1747220": "174",
    "1747230": "174",
    "1747450": "174",
    "1747810": "174",
    "1747990": "174",
    "1747991": "174",
    "1747992": "174",
    "1747993": "174",

    # علم البيانات - 178
    "1781010": "178",
    "1781011": "178",
    "1781020": "178",
    "1781101": "178",
    "1781110": "178",
    "1781120": "178",
    "1782301": "178",
    "1782320": "178",
    "1783210": "178",
    "1783300": "178",
    "1783600": "178",
    "1783950": "178",
    "1784221": "178",
    "1784390": "178",
    "1784500": "178",
    "1784510": "178",
    "1784540": "178",
    "1784580": "178",
    "1784800": "178",
    "1784810": "178",
    "1784930": "178",

    # الذكاء الاصطناعي - 179
    "1792440": "179",
    "1792442": "179",
    "1792450": "179",
    "1792490": "179",
    "1792491": "179",
    "1792750": "179",
    "1793280": "179",
    "1793420": "179",
    "1793750": "179",
    "1793800": "179",
    "1793810": "179",
    "1794450": "179",
    "1794470": "179",
    "1794900": "179",
    "1794910": "179",
    "1794920": "179",

    # نظم المعلومات الصحية - 203
    "2032010": "203",
    "2033210": "203",
    "2033211": "203",
    "2033320": "203",
    "2033321": "203",
    "2033350": "203",
    "2033910": "203",
    "2034200": "203",
    "2034910": "203",
    "2034911": "203",
    "2034920": "203",

    # العلوم الأساسية الإنسانية والعلمية - 82 (العلوم والآداب - 90)
    "821052": "82",
    "821104": "82",
    "821105": "82",
    "821106": "82",
    "821192": "82",
    "821200": "82",
    "821300": "82",
    "821411": "82",
    "821511": "82",
    "821531": "82",
    "822210": "82",
    "822520": "82",
    "823020": "82",

    # علوم العسكرية - 84 (شعبة العلوم العسكرية - 80)
    "841000": "84",
    # عربي - 80
    "801022": "80",
    "801023": "80",
    "802000": "80",
    "802010": "80",
    "802020": "80",
    # هندسة البرمجيات - 176
    "821125": "176",
    "821127": "176",
    "821131": "176",
    "1762100": "176",
    "1762110": "176",
    "1762200": "176",
    "1762300": "176",
    "1763100": "176",
    "1763210": "176",
    "1763231": "176",
    "1763240": "176",
    "1763250": "176",
    "1763710": "176",
    "1763900": "176",
    "1764120": "176",
    "1764300": "176",
    "1764310": "176",
    "1764320": "176",
    "1764400": "176",
    "1764911": "176",
    "1764921": "176",
    "1764950": "176",
    "8210211": "176",
    # الرياضيات - 90
    "821011": "90",
    "821021": "90",
    "821023": "90",
    "821034": "90",
    "821038": "90",
    "822010": "90",
    "822030": "90",
    "822212": "90",
    "822331": "90",
    "822350": "90",
    "822411": "90",
    "900990": "90",
    "901111": "90",
    "901310": "90",
    "901320": "90",
    "901400": "90",
    "901450": "90",
    "902450": "90",
    "903011": "90",
    "903050": "90",
    "903071": "90",
    "903212": "90",
    "903300": "90",
    "903312": "90",
    "903391": "90",
    "903400": "90",
    "903420": "90",
    "903450": "90",
    "903470": "90",
    "903620": "90",
    "904070": "90",
    "904420": "90",
    "904921": "90",
    "904932": "90",
    "904970": "90",
    "904980": "90",
    "907010": "90",
    "907070": "90",
    "907090": "90",
    "907210": "90",
    "907310": "90",
    "907410": "90",
    "907910": "90",
    "907950": "90",
    "907996": "90",
    "907997": "90",
    "907998": "90",
    "907999": "90",
    # اللغة الانجليزية واللغويات - 81
    "812413": "81",
    "812712": "81",
    "813050": "81",
    "813070": "81",
    "813300": "81",
    "813512": "81",
    "813600": "81",
    "813610": "81",
    "813722": "81",
    "813920": "81",
    "814031": "81",
    "814050": "81",
    "814060": "81",
    "814121": "81",
    "814930": "81",
    "817110": "81",
    "817711": "81",
    "817960": "81",
    "817980": "81",
    "817994": "81",
    "817996": "81",
    "817997": "81",
    "817999": "81",
    "871010": "81",
    "871710": "81",
    "872010": "81",
    "2511111": "81",
    # مركز اللغات - -1
    "2510990": "-1",
    "2511010": "-1",
    "2511030": "-1",
    "2511040": "-1",
    "2511050": "-1",
    "2511080": "-1",
    "2515030": "-1"
}

SITE_URL = "https://services.just.edu.jo/courseschedule/"

SITE_CHECK_INTERVAL_SECONDS = 40
RATE_LIMIT_BACKOFF_SECONDS = 92
ERROR_BACKOFF_SECONDS = 60
CHECK_JITTER_SECONDS = 10
DEPARTMENT_CHECK_DELAY_SECONDS = 5
REMOVAL_CONFIRMATION_CHECKS = 2

STATE_FILE = Path("course_states.json")
TARGET_FILE = Path("watched_course.json")
USERS_FILE = Path("users.json")
DEBUG_HTML_FILE = Path("result.html")
DEBUG_SCREENSHOT_FILE = Path("result.png")

DEPARTMENT_CACHE_SECONDS = 8
USER_RATE_LIMIT_WINDOW_SECONDS = 10
USER_RATE_LIMIT_MAX_ACTIONS = 12
ALERT_KEYS = [
    "new_section",
    "became_available",
    "capacity_up",
    "status_closed",
    "removed_section",
    "section_details_changed"
]
DEFAULT_ALERTS = {
    key: True
    for key in ALERT_KEYS
}

DEPARTMENT_CACHE = {}
USER_RATE_STATE = {}
RUNTIME_STATS = {
    "started_at": time.time(),
    "last_success_at": None,
    "last_error": "",
    "total_site_checks": 0,
    "total_department_batches": 0,
    "total_rate_limits": 0,
    "total_recoveries": 0,
}

session = requests.Session()


class RateLimitedError(Exception):
    pass


class VerificationError(Exception):
    pass


def telegram_api(method, params=None, timeout=20):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/{method}"

    response = session.post(
        url,
        data=params or {},
        timeout=timeout
    )

    try:
        data = response.json()
    except Exception:
        data = {
            "ok": False,
            "description": response.text
        }

    return response.status_code, data


def check_telegram():
    if not TELEGRAM_TOKEN:
        print("ERROR: TELEGRAM_TOKEN is empty.")
        return False

    status, data = telegram_api("getMe")

    if not data.get("ok"):
        print(
            "Telegram error:",
            status,
            data.get("description")
        )
        return False

    bot = data.get("result", {})

    print(
        f"Telegram OK: @{bot.get('username', 'unknown')}"
    )

    status, data = telegram_api(
        "getWebhookInfo"
    )

    if data.get("ok"):
        webhook_url = (
            data.get("result", {}).get("url")
            or ""
        )

        if webhook_url:
            status, deleted = telegram_api(
                "deleteWebhook",
                {
                    "drop_pending_updates": "false"
                }
            )

            if not deleted.get("ok"):
                print(
                    "Could not remove webhook:",
                    status,
                    deleted.get("description")
                )
                return False

            print("Webhook removed.")

    return True


TELEGRAM_MAX_TEXT = 4000


def send_message(chat_id, text, reply_markup=None):
    text = str(text)

    chunks = []

    while len(text) > TELEGRAM_MAX_TEXT:
        split_at = text.rfind(
            "\n",
            0,
            TELEGRAM_MAX_TEXT
        )

        if split_at < 500:
            split_at = TELEGRAM_MAX_TEXT

        chunks.append(
            text[:split_at].rstrip()
        )

        text = text[
            split_at:
        ].lstrip()

    if text:
        chunks.append(text)

    if not chunks:
        chunks = [""]

    all_ok = True

    for index, chunk in enumerate(chunks):
        params = {
            "chat_id": chat_id,
            "text": chunk
        }

        # Put the button only on the last message.
        if (
            reply_markup is not None
            and index == len(chunks) - 1
        ):
            params["reply_markup"] = json.dumps(
                reply_markup,
                ensure_ascii=False
            )

        status, data = telegram_api(
            "sendMessage",
            params
        )

        if not data.get("ok"):
            print(
                "Telegram send error:",
                status,
                data.get("description")
            )

            all_ok = False

    return all_ok


def status_keyboard(line=None):
    callback_data = (
        f"update_status:{normalize_text(line)}"
        if line
        else "update_status"
    )

    return {
        "inline_keyboard": [
            [
                {
                    "text": "🔄 تحديث الحالة",
                    "callback_data": callback_data
                }
            ]
        ]
    }


def edit_message(chat_id, message_id, text, reply_markup=None):
    params = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": str(text)
    }

    if reply_markup is not None:
        params["reply_markup"] = json.dumps(
            reply_markup,
            ensure_ascii=False
        )

    status, data = telegram_api(
        "editMessageText",
        params
    )

    if not data.get("ok"):
        print(
            "Telegram edit error:",
            status,
            data.get("description")
        )
        return False

    return True


def answer_callback(callback_id):
    telegram_api(
        "answerCallbackQuery",
        {
            "callback_query_id": callback_id
        }
    )


def get_updates(offset):
    try:
        status, data = telegram_api(
            "getUpdates",
            {
                "offset": offset,
                "timeout": 10,
                "allowed_updates": json.dumps(
                    ["message", "callback_query"]
                )
            },
            timeout=20
        )

        if not data.get("ok"):
            print(
                "Telegram getUpdates error:",
                status,
                data.get("description")
            )
            return [], offset

        updates = data.get("result", [])

        if updates:
            offset = updates[-1]["update_id"] + 1

        return updates, offset

    except Exception as e:
        print(
            "Telegram getUpdates failed:",
            repr(e)
        )
        return [], offset


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            return default

    return default


def save_json(path, data):
    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


def load_target():
    data = load_json(
        TARGET_FILE,
        {
            "chat_id": None,
            "lines": [],
            "line": None,
            "update_offset": 0,
            "mode": None,
            "paused": False
        }
    )

    lines = data.get("lines")

    if not isinstance(lines, list):
        lines = []

    old_line = data.get("line")

    if old_line and not lines:
        lines = [str(old_line)]

    clean_lines = []

    for line in lines:
        line = normalize_text(line)

        if (
            line
            and valid_line(line)
            and line not in clean_lines
        ):
            clean_lines.append(line)

    data["lines"] = clean_lines

    if clean_lines:
        data["line"] = clean_lines[-1]
    else:
        data["line"] = None

    data.setdefault("chat_id", None)
    data.setdefault("update_offset", 0)
    data.setdefault("mode", None)
    data.setdefault("paused", False)
    data.setdefault("ui_action", None)
    data.setdefault("ui_faculty", None)
    data.setdefault("ui_department", None)
    data.setdefault("ui_page", 0)

    return data


def save_target(target):
    save_json(
        TARGET_FILE,
        target
    )


def default_user_state(chat_id=""):
    return {
        "chat_id": str(chat_id),
        "lines": [],
        "line": None,
        "mode": None,
        "paused": False,
        "ui_action": None,
        "ui_faculty": None,
        "ui_department": None,
        "ui_page": 0,
        "alerts": dict(DEFAULT_ALERTS)
    }


def normalize_user_state(chat_id, data):
    user = default_user_state(chat_id)

    if isinstance(data, dict):
        user.update(data)

    user["chat_id"] = str(chat_id)

    lines = user.get("lines", [])
    if not isinstance(lines, list):
        lines = []

    clean_lines = []
    for line in lines:
        line = normalize_text(line)
        if line and valid_line(line) and line not in clean_lines:
            clean_lines.append(line)

    user["lines"] = clean_lines
    user["line"] = clean_lines[-1] if clean_lines else None

    if not isinstance(user.get("ui_page"), int):
        user["ui_page"] = 0

    raw_alerts = user.get("alerts", {})
    if not isinstance(raw_alerts, dict):
        raw_alerts = {}

    alerts = dict(DEFAULT_ALERTS)
    for key in ALERT_KEYS:
        if key in raw_alerts:
            alerts[key] = bool(raw_alerts[key])

    user["alerts"] = alerts

    return user


def load_users():
    data = load_json(
        USERS_FILE,
        {}
    )

    if not isinstance(data, dict):
        data = {}

    raw_users = data.get("users", {})
    if not isinstance(raw_users, dict):
        raw_users = {}

    users = {}
    for chat_id, user_data in raw_users.items():
        users[str(chat_id)] = normalize_user_state(
            chat_id,
            user_data
        )

    offset = data.get("update_offset", 0)
    try:
        offset = int(offset)
    except Exception:
        offset = 0

    if not users:
        legacy = load_target()
        legacy_chat_id = legacy.get("chat_id")

        if legacy_chat_id:
            users[str(legacy_chat_id)] = normalize_user_state(
                legacy_chat_id,
                legacy
            )
            try:
                offset = int(legacy.get("update_offset", 0))
            except Exception:
                offset = 0

    return {
        "users": users,
        "update_offset": offset
    }


def save_users(users_data):
    save_json(
        USERS_FILE,
        users_data
    )


def get_user(users, chat_id):
    key = str(chat_id)

    if key not in users:
        users[key] = default_user_state(key)

    users[key] = normalize_user_state(
        key,
        users[key]
    )

    return users[key]


def all_monitored_lines(users):
    result = []

    for user in users.values():
        for line in monitored_lines(user):
            line = normalize_text(line)
            if line and line not in result:
                result.append(line)

    return result


def active_monitored_lines(users):
    result = []

    for user in users.values():
        if user.get("paused", False):
            continue

        for line in monitored_lines(user):
            line = normalize_text(line)
            if line and line not in result:
                result.append(line)

    return result


def watchers_for_line(users, line, include_paused=False):
    line = normalize_text(line)
    result = []

    for chat_id, user in users.items():
        if not include_paused and user.get("paused", False):
            continue

        if line in monitored_lines(user):
            result.append(str(chat_id))

    return result


def allow_user_action(chat_id):
    now = time.time()
    chat_id = str(chat_id)

    timestamps = USER_RATE_STATE.setdefault(chat_id, [])
    cutoff = now - USER_RATE_LIMIT_WINDOW_SECONDS
    timestamps[:] = [t for t in timestamps if t >= cutoff]

    if len(timestamps) >= USER_RATE_LIMIT_MAX_ACTIONS:
        return False

    timestamps.append(now)
    return True


def alert_enabled(user, event_type):
    alerts = user.get("alerts", {})
    return bool(alerts.get(event_type, DEFAULT_ALERTS.get(event_type, True)))


def event_allowed_for_user(user, event):
    return alert_enabled(
        user,
        event.get("type", "")
    )


def alert_label(key):
    labels = {
        "new_section": "فتح شعبة جديدة",
        "became_available": "شعبة أصبحت متاحة",
        "capacity_up": "رفع السعة",
        "status_closed": "إغلاق/إلغاء شعبة",
        "removed_section": "إزالة شعبة",
        "section_details_changed": "تغيير الأيام/الوقت/القاعة/المدرس"
    }
    return labels.get(key, key)


def settings_keyboard(user):
    rows = []

    for key in ALERT_KEYS:
        enabled = alert_enabled(user, key)
        icon = "✅" if enabled else "❌"
        rows.append([
            {
                "text": f"{icon} {alert_label(key)}",
                "callback_data": f"toggle_alert:{key}"
            }
        ])

    rows.append([
        {
            "text": "♻️ تفعيل جميع التنبيهات",
            "callback_data": "alerts_all_on"
        },
        {
            "text": "🚫 إيقاف جميع التنبيهات",
            "callback_data": "alerts_all_off"
        }
    ])
    rows.append([
        {
            "text": "↩️ القائمة الرئيسية",
            "callback_data": "main_menu"
        }
    ])

    return {"inline_keyboard": rows}


def settings_text(user):
    enabled_count = sum(
        1
        for key in ALERT_KEYS
        if alert_enabled(user, key)
    )

    lines = [
        "⚙️ إعدادات التنبيهات",
        "",
        f"التنبيهات المفعلة: {enabled_count} / {len(ALERT_KEYS)}",
        "",
        "اضغط على أي تنبيه لتفعيله أو إيقافه:"
    ]

    for key in ALERT_KEYS:
        status = "مفعل ✅" if alert_enabled(user, key) else "متوقف ❌"
        lines.append(
            f"• {alert_label(key)} — {status}"
        )

    return "\n".join(lines)


def runtime_uptime_text():
    elapsed = max(0, int(time.time() - RUNTIME_STATS.get("started_at", time.time())))
    days, rem = divmod(elapsed, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, seconds = divmod(rem, 60)

    parts = []
    if days:
        parts.append(f"{days}ي")
    if hours:
        parts.append(f"{hours}س")
    if minutes:
        parts.append(f"{minutes}د")
    parts.append(f"{seconds}ث")
    return " ".join(parts)


def format_runtime_time(timestamp):
    if not timestamp:
        return "غير متاح"

    try:
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    except Exception:
        return "غير متاح"


def dashboard_text(users, course_meta):
    all_lines = all_monitored_lines(users)
    active_lines = active_monitored_lines(users)
    active_users = sum(
        1
        for user in users.values()
        if monitored_lines(user) and not user.get("paused", False)
    )
    departments = {
        key
        for line in active_lines
        if (key := (
            faculty_for_department(department_for_line(line))
            if department_for_line(line)
            else None,
            department_for_line(line)
            if department_for_line(line)
            else None
        )) != (None, None)
    }

    cache_valid = 0
    now = time.time()
    for item in DEPARTMENT_CACHE.values():
        if now - item.get("timestamp", 0) <= DEPARTMENT_CACHE_SECONDS:
            cache_valid += 1

    lines = [
        "📈 لوحة تحكم البوت",
        "━━━━━━━━━━━━━━━━━━━━",
        f"👥 المستخدمون: {len(users)}",
        f"🟢 المستخدمون النشطون: {active_users}",
        f"📚 المواد الفريدة المراقبة: {len(all_lines)}",
        f"🏫 المجموعات النشطة: {len(departments)}",
        f"🗂️ الكاش الفعال: {cache_valid}",
        "",
        f"🔍 فحوصات المواد: {RUNTIME_STATS.get('total_site_checks', 0)}",
        f"📦 دفعات الأقسام: {RUNTIME_STATS.get('total_department_batches', 0)}",
        f"⚠️ مرات Rate Limit: {RUNTIME_STATS.get('total_rate_limits', 0)}",
        f"♻️ مرات الاسترداد: {RUNTIME_STATS.get('total_recoveries', 0)}",
        "",
        f"⏱️ وقت التشغيل: {runtime_uptime_text()}",
        f"✅ آخر فحص ناجح: {format_runtime_time(RUNTIME_STATS.get('last_success_at'))}",
    ]

    last_error = RUNTIME_STATS.get("last_error") or "لا يوجد"
    lines.append(f"🛑 آخر خطأ: {last_error}")

    return "\n".join(lines)


def get_cached_department_html(faculty_value, dept_value):
    key = (str(faculty_value), str(dept_value))
    item = DEPARTMENT_CACHE.get(key)

    if not item:
        return None

    if time.time() - item.get("timestamp", 0) > DEPARTMENT_CACHE_SECONDS:
        DEPARTMENT_CACHE.pop(key, None)
        return None

    return item.get("html")


def cache_department_html(faculty_value, dept_value, html):
    DEPARTMENT_CACHE[(str(faculty_value), str(dept_value))] = {
        "timestamp": time.time(),
        "html": html
    }


def deduplicate_events(events):
    result = []

    available_sections = {
        e.get("section")
        for e in events
        if e.get("type") == "became_available"
    }

    closed_sections = {
        e.get("section")
        for e in events
        if e.get("type") == "status_closed"
    }

    seen = set()

    for event in events:
        event_type = event.get("type")
        section = event.get("section")

        if (event_type, section) in seen:
            continue

        if event_type == "capacity_up" and section in available_sections:
            continue

        if event_type == "section_details_changed" and section in (
            available_sections | closed_sections
        ):
            continue

        seen.add((event_type, section))
        result.append(event)

    return result


def normalize_text(value):
    if value is None:
        return ""

    value = str(value)

    value = value.translate(
        str.maketrans(
            "٠١٢٣٤٥٦٧٨٩",
            "0123456789"
        )
    )

    value = value.replace(
        "\u200f",
        " "
    )

    value = value.replace(
        "\u200e",
        " "
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def valid_line(text):
    text = normalize_text(text)

    return bool(
        re.fullmatch(
            r"\d{4,12}",
            text
        )
    )


def direct_cells(row):
    cells = row.find_all(
        ["td", "th"],
        recursive=False
    )

    if cells:
        return [
            normalize_text(
                cell.get_text(
                    " ",
                    strip=True
                )
            )
            for cell in cells
        ]

    return [
        normalize_text(
            cell.get_text(
                " ",
                strip=True
            )
        )
        for cell in row.find_all(
            ["td", "th"]
        )
    ]


def is_section_header_row(row):
    cells = direct_cells(row)

    if not cells:
        return False

    joined = " ".join(cells).lower()

    has_section = (
        "الشعبة" in joined
        or "section" in joined
    )

    has_registered = (
        "مسجلين" in joined
        or "registered" in joined
        or "enrolled" in joined
    )

    has_capacity = (
        "سعة" in joined
        or "capacity" in joined
    )

    return (
        has_section
        and has_registered
        and has_capacity
    )


def find_course_blocks(soup, target_line):
    target_line = normalize_text(
        target_line
    )

    candidates = []

    label_patterns = [
        rf"(?:رقم\s*السطر|رقم\s*السطر\s*)\s*:?\s*{re.escape(target_line)}\b",
        rf"(?:row\s*number|line\s*number)\s*:?\s*{re.escape(target_line)}\b"
    ]

    for cell in soup.find_all(
        ["td", "th"]
    ):
        cell_text = normalize_text(
            cell.get_text(
                " ",
                strip=True
            )
        )

        if not any(
            re.search(
                pattern,
                cell_text,
                flags=re.IGNORECASE
            )
            for pattern in label_patterns
        ):
            continue

        row = cell.find_parent("tr")

        if row is None:
            continue

        section_tables = []

        for table in row.find_all(
            "table"
        ):
            for header_row in table.find_all("tr"):
                if is_section_header_row(
                    header_row
                ):
                    section_tables.append(
                        table
                    )
                    break

        # Strong preference for the exact course row that
        # contains the nested sections table.
        score = (
            1 if section_tables else 0,
            -len(
                row.get_text(
                    " ",
                    strip=True
                )
            ),
            len(section_tables)
        )

        candidates.append(
            (
                score,
                row,
                cell,
                section_tables
            )
        )

    candidates.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return candidates


def extract_course_metadata(info_cell, target_line):
    text = normalize_text(
        info_cell.get_text(
            " ",
            strip=True
        )
    )

    def extract(patterns):
        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if match:
                value = normalize_text(
                    match.group(1)
                )

                if value:
                    return value

        return ""

    code = extract(
        [
            r"رمز\s*المساق\s*:?\s*(.+?)(?=\s+(?:اسم\s*المساق|الساعات|رقم\s*السطر)\b|$)",
            r"course\s*(?:code|id)\s*:?\s*(.+?)(?=\s+(?:course\s*name|credit|hours|row\s*number)\b|$)"
        ]
    )

    title = extract(
        [
            r"اسم\s*المساق\s*:?\s*(.+?)(?=\s+(?:الساعات|رقم\s*السطر|رمز\s*المساق)\b|$)",
            r"اسم\s*المادة\s*:?\s*(.+?)(?=\s+(?:الساعات|رقم\s*السطر|رمز\s*المساق)\b|$)",
            r"course\s*name\s*:?\s*(.+?)(?=\s+(?:credit|hours|row\s*number|course\s*code)\b|$)"
        ]
    )

    hours = extract(
        [
            r"الساعات\s*:?\s*(\d+(?:\.\d+)?)",
            r"(?:credit|hours)\s*:?\s*(\d+(?:\.\d+)?)"
        ]
    )

    row_number = extract(
        [
            r"رقم\s*السطر\s*:?\s*(\d{4,12})",
            r"(?:row|line)\s*number\s*:?\s*(\d{4,12})"
        ]
    )

    if not row_number:
        row_number = target_line

    return {
        "line": row_number,
        "code": code,
        "title": title,
        "hours": hours
    }


def get_column_index(header_cells, keywords):
    for i, cell in enumerate(
        header_cells
    ):
        cell_low = normalize_text(
            cell
        ).lower()

        for keyword in keywords:
            if keyword.lower() in cell_low:
                return i

    return None


def parse_section_table(table):
    rows = table.find_all(
        "tr"
    )

    header_row = None
    header_cells = []

    for row in rows:
        if is_section_header_row(
            row
        ):
            header_row = row
            header_cells = direct_cells(
                row
            )
            break

    if header_row is None:
        return []

    idx_section = get_column_index(
        header_cells,
        [
            "الشعبة",
            "section"
        ]
    )

    idx_days = get_column_index(
        header_cells,
        [
            "الأيام",
            "days",
            "day"
        ]
    )

    idx_time = get_column_index(
        header_cells,
        [
            "الوقت",
            "time"
        ]
    )

    idx_room = get_column_index(
        header_cells,
        [
            "قاعة",
            "room"
        ]
    )

    idx_instructor = get_column_index(
        header_cells,
        [
            "المدرس",
            "مدرس",
            "المحاضر",
            "الاستاذ",
            "instructor",
            "teacher",
            "lecturer"
        ]
    )

    idx_registered = get_column_index(
        header_cells,
        [
            "مسجلين",
            "registered",
            "enrolled"
        ]
    )

    idx_capacity = get_column_index(
        header_cells,
        [
            "سعة",
            "capacity"
        ]
    )

    idx_status = get_column_index(
        header_cells,
        [
            "الحالة",
            "حالة الشعبة",
            "status",
            "section status"
        ]
    )

    if (
        idx_section is None
        or idx_registered is None
        or idx_capacity is None
    ):
        return []

    sections = []
    started = False

    for row in rows:
        if row is header_row:
            started = True
            continue

        if not started:
            continue

        cells = direct_cells(
            row
        )

        if len(cells) <= max(
            idx_section,
            idx_registered,
            idx_capacity
        ):
            continue

        section = normalize_text(
            cells[idx_section]
        )

        registered_match = re.search(
            r"\d+",
            normalize_text(
                cells[idx_registered]
            )
        )

        capacity_match = re.search(
            r"\d+",
            normalize_text(
                cells[idx_capacity]
            )
        )

        if (
            not registered_match
            or not capacity_match
        ):
            continue

        status = ""
        days = ""
        section_time = ""
        room = ""
        instructor = ""

        if (
            idx_instructor is not None
            and idx_instructor < len(cells)
        ):
            instructor = normalize_text(
                cells[idx_instructor]
            )

        if (
            idx_status is not None
            and idx_status < len(cells)
        ):
            status = normalize_text(
                cells[idx_status]
            )

        if (
            idx_days is not None
            and idx_days < len(cells)
        ):
            days = normalize_text(
                cells[idx_days]
            )

        if (
            idx_time is not None
            and idx_time < len(cells)
        ):
            section_time = normalize_text(
                cells[idx_time]
            )

        if (
            idx_room is not None
            and idx_room < len(cells)
        ):
            room = normalize_text(
                cells[idx_room]
            )

        sections.append(
            {
                "section": section or "?",
                "days": days,
                "time": section_time,
                "room": room,
                "instructor": instructor,
                "registered": int(
                    registered_match.group()
                ),
                "capacity": int(
                    capacity_match.group()
                ),
                "status": status
            }
        )

    return sections


def parse_course(html, target_line):
    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    target_line = normalize_text(
        target_line
    )

    candidates = find_course_blocks(
        soup,
        target_line
    )

    if not candidates:
        return None

    for (
        score,
        course_row,
        info_cell,
        section_tables
    ) in candidates:

        metadata = extract_course_metadata(
            info_cell,
            target_line
        )

        # The screenshot shows one nested table for the
        # sections inside the exact course block.
        for table in section_tables:
            sections = parse_section_table(
                table
            )

            if not sections:
                continue

            return {
                "line": target_line,
                "code": metadata["code"],
                "title": metadata["title"],
                "hours": metadata["hours"],
                "sections": sections
            }

    return None



def snapshot(course):
    result = {}

    for section in course["sections"]:
        key = normalize_text(
            section["section"]
        )

        result[key] = {
            "days": section.get("days", ""),
            "time": section.get("time", ""),
            "room": section.get("room", ""),
            "instructor": section.get("instructor", ""),
            "registered": section["registered"],
            "capacity": section["capacity"],
            "status": section["status"]
        }

    return result


def is_closed_status(status):
    status = normalize_text(
        status
    ).lower()

    closed_words = [
        "مغلقة",
        "مغلق",
        "ملغاة",
        "ملغى",
        "closed",
        "cancelled",
        "canceled"
    ]

    return any(
        word in status
        for word in closed_words
    )


def section_is_open(data):
    status = normalize_text(
        data.get("status", "")
    )

    if is_closed_status(status):
        return False

    return data["registered"] < data["capacity"]


def compare_course(old, new):
    events = []

    old_sections = set(old.keys())
    new_sections = set(new.keys())

    for section in sorted(
        new_sections - old_sections
    ):
        data = new[section]

        events.append(
            {
                "type": "new_section",
                "section": section,
                "days": data.get("days", ""),
                "time": data.get("time", ""),
                "room": data.get("room", ""),
                "registered": data["registered"],
                "capacity": data["capacity"],
                "status": data["status"]
            }
        )

    for section in sorted(
        old_sections - new_sections
    ):
        events.append(
            {
                "type": "removed_section",
                "section": section,
                "old": old[section]
            }
        )

    for section in sorted(
        old_sections & new_sections
    ):
        old_data = old[section]
        new_data = new[section]

        old_open = section_is_open(
            old_data
        )

        new_open = section_is_open(
            new_data
        )

        # A full/closed section became available.
        if (
            not old_open
            and new_open
        ):
            events.append(
                {
                    "type": "became_available",
                    "section": section,
                    "old_registered": old_data["registered"],
                    "old_capacity": old_data["capacity"],
                    "new_registered": new_data["registered"],
                    "new_capacity": new_data["capacity"],
                    "new_status": new_data["status"],
                    "days": new_data.get("days", ""),
                    "time": new_data.get("time", ""),
                    "room": new_data.get("room", "")
                }
            )

        # Capacity was increased.
        if (
            new_data["capacity"]
            > old_data["capacity"]
        ):
            events.append(
                {
                    "type": "capacity_up",
                    "section": section,
                    "old_capacity": old_data["capacity"],
                    "new_capacity": new_data["capacity"],
                    "registered": new_data["registered"],
                    "days": new_data.get("days", ""),
                    "time": new_data.get("time", ""),
                    "room": new_data.get("room", "")
                }
            )

        # Explicitly changed to a closed/cancelled status.
        if (
            is_closed_status(
                new_data["status"]
            )
            and not is_closed_status(
                old_data["status"]
            )
        ):
            events.append(
                {
                    "type": "status_closed",
                    "section": section,
                    "status": new_data["status"],
                    "days": new_data.get("days", ""),
                    "time": new_data.get("time", ""),
                    "room": new_data.get("room", ""),
                    "instructor": new_data.get("instructor", "")
                }
            )

        changed_fields = {}
        for field, label in (
            ("days", "الأيام"),
            ("time", "الوقت"),
            ("room", "القاعة"),
            ("instructor", "المدرس")
        ):
            old_value = normalize_text(old_data.get(field, ""))
            new_value = normalize_text(new_data.get(field, ""))

            if old_value != new_value:
                changed_fields[label] = {
                    "old": old_value,
                    "new": new_value
                }

        if changed_fields:
            events.append(
                {
                    "type": "section_details_changed",
                    "section": section,
                    "changes": changed_fields,
                    "days": new_data.get("days", ""),
                    "time": new_data.get("time", ""),
                    "room": new_data.get("room", ""),
                    "instructor": new_data.get("instructor", "")
                }
            )

    return deduplicate_events(events)



def get_section_status(section):
    site_status = normalize_text(
        section.get("status", "")
    )

    if is_closed_status(
        site_status
    ):
        return "مغلقة"

    if section["registered"] >= section["capacity"]:
        return "مغلقة"

    return "مفتوحة"


def format_section_details(section):
    status = get_section_status(
        section
    )

    icon = (
        "🟢"
        if status == "مفتوحة"
        else "🔴"
    )

    remaining = max(
        section["capacity"] - section["registered"],
        0
    )

    lines = [
        f"{icon} الشعبة {section['section']} — {status}",
    ]

    days = section.get("days", "")
    section_time = section.get("time", "")
    room = section.get("room", "")
    instructor = section.get("instructor", "")

    if days:
        lines.append(
            f"   الأيام: {days}"
        )

    if section_time:
        lines.append(
            f"   الوقت: {section_time}"
        )

    if room:
        lines.append(
            f"   القاعة: {room}"
        )

    if instructor:
        lines.append(
            f"   المدرس: {instructor}"
        )

    lines.append(
        f"   المقاعد المتبقية: {remaining}"
    )
    lines.append(
        f"   المسجلون: {section['registered']} / {section['capacity']}"
    )

    if section.get("status"):
        lines.append(
            f"   حالة الموقع: {section['status']}"
        )

    return lines


def event_location_lines(data):
    lines = []

    if data.get("days"):
        lines.append(
            f"الأيام: {data['days']}"
        )

    if data.get("time"):
        lines.append(
            f"الوقت: {data['time']}"
        )

    if data.get("room"):
        lines.append(
            f"القاعة: {data['room']}"
        )

    if data.get("instructor"):
        lines.append(
            f"المدرس: {data['instructor']}"
        )

    return lines


def format_initial_status(course):
    title = (
        course.get("title")
        or "غير معروف"
    )

    code_value = (
        course.get("code")
        or "غير معروف"
    )

    hours = (
        course.get("hours")
        or "غير معروف"
    )

    lines = [
        "📚 بيانات المادة",
        "━━━━━━━━━━━━━━━━━━━━",
        f"اسم المساق: {title}",
        f"رمز المساق: {code_value}",
        f"رقم السطر: {course['line']}",
        f"الساعات: {hours}",
        "",
        f"📋 الشعب ({len(course['sections'])}):",
        ""
    ]

    for index, section in enumerate(
        course["sections"]
    ):
        lines.extend(
            format_section_details(
                section
            )
        )
        if index < len(course["sections"]) - 1:
            lines.append("")

    lines.extend(
        [
            "",
            "━━━━━━━━━━━━━━━━━━━━",
            "✅ المراقبة مفعلة",
            f"الفحص كل حوالي {SITE_CHECK_INTERVAL_SECONDS} ثانية."
        ]
    )

    return "\n".join(lines)


def format_event(course, event):
    title = (
        course.get("title")
        or "غير معروف"
    )

    code_value = (
        course.get("code")
        or ""
    )

    line = course["line"]

    identity = [
        f"المادة: {title}",
        f"رمز المساق: {code_value}",
        f"رقم السطر: {line}",
        f"الشعبة: {event['section']}"
    ]

    if event["type"] == "new_section":
        header = "🟢 فتح شعبة جديدة"
        body = [
            *identity,
            *event_location_lines(event),
            f"المسجلون: {event['registered']} / {event['capacity']}",
            "الحالة: مفتوحة"
        ]
        return header + "\n\n" + "\n".join(body)

    if event["type"] == "became_available":
        header = "🟢 شعبة أصبحت متاحة للتسجيل"
        body = [
            *identity,
            *event_location_lines(event),
            f"المسجلون: {event['new_registered']} / {event['new_capacity']}",
            "الحالة: مفتوحة ✅"
        ]
        return header + "\n\n" + "\n".join(body)

    if event["type"] == "capacity_up":
        header = "🔶 تم رفع سعة شعبة"
        body = [
            *identity,
            *event_location_lines(event),
            f"السعة: {event['old_capacity']} → {event['new_capacity']}",
            f"المسجلون: {event['registered']}"
        ]
        return header + "\n\n" + "\n".join(body)

    if event["type"] == "removed_section":
        old_data = event["old"]
        header = "❌ تم إغلاق/إلغاء شعبة"
        body = [
            *identity,
            *event_location_lines(old_data),
            f"آخر سعة معروفة: {old_data['capacity']}",
            f"آخر عدد مسجلين: {old_data['registered']}"
        ]
        return header + "\n\n" + "\n".join(body)

    if event["type"] == "status_closed":
        header = "❌ تم إغلاق/إلغاء شعبة"
        body = [
            *identity,
            *event_location_lines(event),
            f"الحالة: {event['status'] or 'مغلقة'}"
        ]
        return header + "\n\n" + "\n".join(body)

    if event["type"] == "section_details_changed":
        header = "🟡 تم تغيير بيانات شعبة"
        body = [
            *identity
        ]

        for label, change in event.get("changes", {}).items():
            old_value = change.get("old") or "غير محدد"
            new_value = change.get("new") or "غير محدد"
            body.append(
                f"{label}: {old_value} → {new_value}"
            )

        return header + "\n\n" + "\n".join(body)

    return ""


def main_keyboard():
    return {
        "inline_keyboard": [
            [
                {"text": "➕ إضافة مادة", "callback_data": "add_start"},
                {"text": "🗑️ حذف مادة", "callback_data": "remove_start"}
            ],
            [
                {"text": "📋 المواد المراقبة", "callback_data": "show_list"},
                {"text": "📊 الحالة", "callback_data": "show_status"}
            ],
            [
                {"text": "📈 لوحة التحكم", "callback_data": "show_dashboard"},
                {"text": "⚙️ الإعدادات", "callback_data": "settings"}
            ],
            [
                {"text": "⏸️ إيقاف", "callback_data": "pause_monitor"},
                {"text": "▶️ استئناف", "callback_data": "resume_monitor"}
            ],
            [
                {"text": "❓ المساعدة", "callback_data": "show_help"}
            ]
        ]
    }


def faculty_keyboard():
    return {
        "inline_keyboard": [
            [{"text": FACULTY_NAMES["70"], "callback_data": "add_faculty:70"}],
            [{"text": FACULTY_NAMES["90"], "callback_data": "add_faculty:90"}],
            [{"text": FACULTY_NAMES["80"], "callback_data": "add_faculty:80"}],
            [{"text": "↩️ القائمة الرئيسية", "callback_data": "main_menu"}]
        ]
    }


def departments_for_faculty(faculty_value):
    faculty_value = str(faculty_value)
    values = []
    for dept_value, mapped_faculty in DEPARTMENT_FACULTIES.items():
        if str(mapped_faculty) == faculty_value and any(str(d) == str(dept_value) for d in COURSE_DEPARTMENTS.values()):
            values.append(str(dept_value))
    return sorted(values, key=int)


def department_keyboard(faculty_value):
    rows = []
    for dept_value in departments_for_faculty(faculty_value):
        rows.append([{
            "text": department_name(dept_value),
            "callback_data": f"add_dept:{faculty_value}:{dept_value}"
        }])
    rows.append([{"text": "↩️ رجوع للكليات", "callback_data": "add_start"}])
    return {"inline_keyboard": rows}


def courses_for_department(dept_value):
    lines = [line for line, mapped in COURSE_DEPARTMENTS.items() if str(mapped) == str(dept_value)]
    return sorted(lines, key=int)


def add_course_keyboard(faculty_value, dept_value, page=0):
    per_page = 8
    courses = courses_for_department(dept_value)
    total_pages = max(1, (len(courses) + per_page - 1) // per_page)
    page = max(0, min(int(page), total_pages - 1))
    page_courses = courses[page * per_page:(page + 1) * per_page]
    rows = []
    for line in page_courses:
        title = COURSE_NAMES.get(str(line), "مادة غير معروفة")
        rows.append([{
            "text": f"📚 {title} — {line}",
            "callback_data": f"add_course:{line}"
        }])
    nav=[]
    if page>0:
        nav.append({"text":"⬅️ السابق","callback_data":f"add_page:{faculty_value}:{dept_value}:{page-1}"})
    if page<total_pages-1:
        nav.append({"text":"التالي ➡️","callback_data":f"add_page:{faculty_value}:{dept_value}:{page+1}"})
    if nav: rows.append(nav)
    rows.append([{"text":"↩️ رجوع للأقسام","callback_data":f"add_faculty:{faculty_value}"}])
    return {"inline_keyboard":rows}


def remove_keyboard(lines, page=0):
    per_page=10
    lines=list(lines)
    total_pages=max(1,(len(lines)+per_page-1)//per_page)
    page=max(0,min(int(page),total_pages-1))
    page_lines=lines[page*per_page:(page+1)*per_page]
    rows=[]
    for line in page_lines:
        title=COURSE_NAMES.get(str(line), "")
        label=f"🗑️ {title} — {line}" if title else f"🗑️ {line}"
        rows.append([{"text":label,"callback_data":f"remove_course:{line}"}])
    nav=[]
    if page>0: nav.append({"text":"⬅️ السابق","callback_data":f"remove_page:{page-1}"})
    if page<total_pages-1: nav.append({"text":"التالي ➡️","callback_data":f"remove_page:{page+1}"})
    if nav: rows.append(nav)
    rows.append([{"text":"↩️ القائمة الرئيسية","callback_data":"main_menu"}])
    return {"inline_keyboard":rows}


def add_menu_text(faculty_value=None, dept_value=None, page=0):
    if faculty_value is None:
        return "➕ إضافة مادة للمراقبة\n\nاختر الكلية التي تنتمي إليها المادة:"
    if dept_value is None:
        return ("🏫 اختر القسم\n\n" +
                f"الكلية: {FACULTY_NAMES.get(str(faculty_value), faculty_value)}\n\n" +
                "اختر القسم:")
    courses=courses_for_department(dept_value)
    per_page=8
    total_pages=max(1,(len(courses)+per_page-1)//per_page)
    page=max(0,min(int(page),total_pages-1))
    return ("📚 اختر المادة\n\n" +
            f"الكلية: {FACULTY_NAMES.get(str(faculty_value), faculty_value)}\n" +
            f"القسم: {department_name(dept_value)}\n" +
            f"الصفحة {page+1} من {total_pages}\n\n" +
            "اضغط على المادة التي تريد مراقبتها:")


def remove_menu_text(lines, page=0):
    per_page=10
    total_pages=max(1,(len(lines)+per_page-1)//per_page)
    page=max(0,min(int(page),total_pages-1))
    return ("🗑️ حذف مادة من المراقبة\n\n" +
            f"عندك {len(lines)} مادة قيد المراقبة.\n" +
            f"الصفحة {page+1} من {total_pages}\n\n" +
            "اضغط على المادة التي تريد حذفها:")


def help_text():
    return (
        "🤖 بوت مراقبة مواد JUST\n\n"
        "➕ إضافة مادة: اختر الكلية ثم القسم ثم المادة.\n"
        "🗑️ حذف مادة: اختر المادة مباشرة من قائمة المراقبة.\n"
        "📋 /list — عرض المواد التي أراقبها.\n"
        "📊 /status — عرض آخر حالة محفوظة.\n"
        "🔄 /update — تحديث الحالة.\n"
        "⏸️ /stop — إيقاف المراقبة مؤقتاً.\n"
        "▶️ /resume — استئناف المراقبة.\n"
        "🛑 /end — إنهاء المراقبة وحذف المواد.\n"
        "⚙️ /settings — إعدادات التنبيهات.\n"
        "📈 /dashboard — معلومات تشغيل البوت.\n"
        "❓ /help — عرض المساعدة.\n\n"
        "يمكنك استخدام الأزرار بدل كتابة الأوامر."
    )


def known_course_line(line):
    line = normalize_text(line)
    return line in COURSE_DEPARTMENTS


def department_for_line(line):
    line = normalize_text(line)
    return COURSE_DEPARTMENTS.get(line)


def department_name(dept_value):
    return DEPARTMENT_NAMES.get(
        str(dept_value),
        f"القسم {dept_value}"
    )


def faculty_for_department(dept_value):
    return DEPARTMENT_FACULTIES.get(
        str(dept_value),
        FACULTY_VALUE
    )


def group_lines_by_department(lines):
    groups = {}

    for line in lines:
        dept_value = department_for_line(line)

        if not dept_value:
            continue

        faculty_value = faculty_for_department(
            dept_value
        )

        key = (
            faculty_value,
            dept_value
        )

        groups.setdefault(
            key,
            []
        ).append(line)

    return groups


def monitored_lines(target):
    return list(
        target.get(
            "lines",
            []
        )
    )


def set_mode(target, mode):
    target["mode"] = mode
    save_target(target)


def add_line(target, line):
    line = normalize_text(line)

    lines = target.setdefault(
        "lines",
        []
    )

    if line not in lines:
        lines.append(line)

    target["line"] = line
    target["mode"] = None

    return line


def remove_line(target, line):
    line = normalize_text(line)

    lines = target.get(
        "lines",
        []
    )

    target["lines"] = [
        x for x in lines
        if str(x) != str(line)
    ]

    target["line"] = (
        target["lines"][-1]
        if target["lines"]
        else None
    )

    target["mode"] = None

    return line


def format_saved_status(line, snapshot_data):
    if not snapshot_data:
        return (
            f"📌 رقم السطر: {line}\n"
            "لا توجد حالة محفوظة بعد."
        )

    lines = [
        f"📚 آخر حالة محفوظة للمادة {line}",
        ""
    ]

    for index, (section, data) in enumerate(
        snapshot_data.items()
    ):
        section_data = {
            "days": data.get("days", ""),
            "time": data.get("time", ""),
            "room": data.get("room", ""),
            "instructor": data.get("instructor", ""),
            "registered": data.get(
                "registered",
                0
            ),
            "capacity": data.get(
                "capacity",
                0
            ),
            "status": data.get(
                "status",
                ""
            )
        }

        lines.extend(
            format_section_details(
                {
                    "section": section,
                    **section_data
                }
            )
        )

        if index < len(snapshot_data) - 1:
            lines.append("")

    return "\n".join(lines)


def handle_commands(
    users_data,
    states,
    missing_counts,
    course_meta,
    manual_update_times
):
    updates, offset = get_updates(
        users_data.get(
            "update_offset",
            0
        )
    )

    users_data["update_offset"] = offset
    users = users_data.setdefault("users", {})

    force_requests = []
    changed = False
    current_time = time.time()

    def add_force(line, chat_id, mode="check"):
        line = normalize_text(line)
        chat_id = str(chat_id)

        item = {
            "line": line,
            "chat_id": chat_id,
            "mode": mode
        }

        if (
            line
            and not any(
                x["line"] == line
                and x["chat_id"] == chat_id
                and x["mode"] == mode
                for x in force_requests
            )
        ):
            force_requests.append(item)

    for update in updates:
        if "callback_query" in update:
            callback = update.get(
                "callback_query",
                {}
            )

            callback_id = callback.get("id")
            callback_data = (
                callback.get("data")
                or ""
            )

            callback_message = callback.get(
                "message",
                {}
            )

            callback_chat = callback_message.get(
                "chat",
                {}
            )

            callback_chat_id = str(
                callback_chat.get(
                    "id",
                    ""
                )
            )

            if callback_id:
                answer_callback(
                    callback_id
                )

            if not callback_chat_id:
                continue

            if not allow_user_action(callback_chat_id):
                send_message(
                    callback_chat_id,
                    "⏳ طلبات كثيرة خلال ثوانٍ قليلة. انتظر قليلاً ثم جرّب مرة أخرى."
                )
                continue

            target = get_user(
                users,
                callback_chat_id
            )

            if callback_data == "main_menu":
                target["ui_action"] = None
                target["ui_faculty"] = None
                target["ui_department"] = None
                target["ui_page"] = 0
                target["mode"] = None
                send_message(
                    callback_chat_id,
                    "🏠 القائمة الرئيسية",
                    reply_markup=main_keyboard()
                )
                changed = True
                continue

            if callback_data == "add_start":
                target["ui_action"] = "add"
                target["ui_faculty"] = None
                target["ui_department"] = None
                target["ui_page"] = 0
                target["mode"] = None
                send_message(
                    callback_chat_id,
                    add_menu_text(),
                    reply_markup=faculty_keyboard()
                )
                changed = True
                continue

            if callback_data.startswith("add_faculty:"):
                parts = callback_data.split(":")
                if len(parts) == 2 and parts[1] in FACULTY_NAMES:
                    faculty_value = parts[1]
                    target["ui_action"] = "add"
                    target["ui_faculty"] = faculty_value
                    target["ui_department"] = None
                    target["ui_page"] = 0
                    send_message(
                        callback_chat_id,
                        add_menu_text(faculty_value),
                        reply_markup=department_keyboard(faculty_value)
                    )
                    changed = True
                continue

            if callback_data.startswith("add_dept:"):
                parts = callback_data.split(":")
                if len(parts) == 3:
                    faculty_value, dept_value = parts[1], parts[2]
                    if (
                        faculty_value in FACULTY_NAMES
                        and str(DEPARTMENT_FACULTIES.get(dept_value)) == faculty_value
                        and dept_value in departments_for_faculty(faculty_value)
                    ):
                        target["ui_action"] = "add"
                        target["ui_faculty"] = faculty_value
                        target["ui_department"] = dept_value
                        target["ui_page"] = 0
                        send_message(
                            callback_chat_id,
                            add_menu_text(
                                faculty_value,
                                dept_value,
                                0
                            ),
                            reply_markup=add_course_keyboard(
                                faculty_value,
                                dept_value,
                                0
                            )
                        )
                        changed = True
                continue

            if callback_data.startswith("add_page:"):
                parts = callback_data.split(":")
                if len(parts) == 4:
                    faculty_value, dept_value = parts[1], parts[2]
                    try:
                        page = int(parts[3])
                    except ValueError:
                        page = 0

                    if (
                        faculty_value in FACULTY_NAMES
                        and dept_value in departments_for_faculty(faculty_value)
                    ):
                        target["ui_action"] = "add"
                        target["ui_faculty"] = faculty_value
                        target["ui_department"] = dept_value
                        target["ui_page"] = page
                        send_message(
                            callback_chat_id,
                            add_menu_text(
                                faculty_value,
                                dept_value,
                                page
                            ),
                            reply_markup=add_course_keyboard(
                                faculty_value,
                                dept_value,
                                page
                            )
                        )
                        changed = True
                continue

            if callback_data.startswith("add_course:"):
                line = normalize_text(
                    callback_data.split(":", 1)[1]
                )

                if known_course_line(line):
                    if line in monitored_lines(target):
                        send_message(
                            callback_chat_id,
                            f"ℹ️ المادة {COURSE_NAMES.get(line, line)} موجودة أصلاً في قائمة المراقبة.",
                            reply_markup=main_keyboard()
                        )
                    else:
                        add_line(
                            target,
                            line
                        )
                        add_force(
                            line,
                            callback_chat_id,
                            "initial"
                        )
                        changed = True
                        send_message(
                            callback_chat_id,
                            "✅ تمت إضافة المادة للمراقبة.\n\n"
                            f"📚 {COURSE_NAMES.get(line, line)}\n"
                            f"🔢 رقم السطر: {line}\n\n"
                            "🔄 جاري جلب حالتها الآن...",
                            reply_markup=main_keyboard()
                        )
                else:
                    send_message(
                        callback_chat_id,
                        "❌ هذه المادة غير موجودة ضمن المواد المدعومة."
                    )
                continue

            if callback_data == "remove_start":
                lines = monitored_lines(target)
                target["ui_action"] = "remove"
                target["ui_page"] = 0
                target["mode"] = None

                if not lines:
                    send_message(
                        callback_chat_id,
                        "📭 لا توجد مواد قيد المراقبة.\n\nأضف مادة أولاً.",
                        reply_markup=main_keyboard()
                    )
                else:
                    send_message(
                        callback_chat_id,
                        remove_menu_text(lines, 0),
                        reply_markup=remove_keyboard(lines, 0)
                    )
                changed = True
                continue

            if callback_data.startswith("remove_page:"):
                try:
                    page = int(
                        callback_data.split(":", 1)[1]
                    )
                except ValueError:
                    page = 0

                lines = monitored_lines(target)
                target["ui_action"] = "remove"
                target["ui_page"] = page
                send_message(
                    callback_chat_id,
                    remove_menu_text(lines, page),
                    reply_markup=remove_keyboard(lines, page)
                )
                changed = True
                continue

            if callback_data.startswith("remove_course:"):
                line = normalize_text(
                    callback_data.split(":", 1)[1]
                )

                if line in monitored_lines(target):
                    title = COURSE_NAMES.get(line, line)
                    remove_line(
                        target,
                        line
                    )
                    target["ui_action"] = None
                    target["ui_page"] = 0
                    changed = True

                    if not watchers_for_line(users, line):
                        states.pop(line, None)
                        missing_counts.pop(line, None)
                        course_meta.pop(line, None)

                    send_message(
                        callback_chat_id,
                        "✅ تم حذف المادة من المراقبة.\n\n"
                        f"📚 {title}\n"
                        f"🔢 رقم السطر: {line}",
                        reply_markup=main_keyboard()
                    )
                else:
                    send_message(
                        callback_chat_id,
                        "ℹ️ هذه المادة لم تعد موجودة في قائمة المراقبة.",
                        reply_markup=main_keyboard()
                    )
                continue

            if callback_data == "settings":
                target["mode"] = None
                target["ui_action"] = "settings"
                send_message(
                    callback_chat_id,
                    settings_text(target),
                    reply_markup=settings_keyboard(target)
                )
                changed = True
                continue

            if callback_data.startswith("toggle_alert:"):
                key = callback_data.split(":", 1)[1]
                if key in ALERT_KEYS:
                    target.setdefault("alerts", dict(DEFAULT_ALERTS))
                    target["alerts"][key] = not alert_enabled(target, key)
                    send_message(
                        callback_chat_id,
                        settings_text(target),
                        reply_markup=settings_keyboard(target)
                    )
                    changed = True
                continue

            if callback_data == "alerts_all_on":
                target["alerts"] = dict(DEFAULT_ALERTS)
                send_message(
                    callback_chat_id,
                    settings_text(target),
                    reply_markup=settings_keyboard(target)
                )
                changed = True
                continue

            if callback_data == "alerts_all_off":
                target["alerts"] = {key: False for key in ALERT_KEYS}
                send_message(
                    callback_chat_id,
                    settings_text(target),
                    reply_markup=settings_keyboard(target)
                )
                changed = True
                continue

            if callback_data == "show_dashboard":
                target["mode"] = None
                target["ui_action"] = "dashboard"
                send_message(
                    callback_chat_id,
                    dashboard_text(users, course_meta),
                    reply_markup=main_keyboard()
                )
                changed = True
                continue

            if callback_data == "show_list":
                lines = monitored_lines(target)

                if not lines:
                    send_message(
                        callback_chat_id,
                        "📭 لا توجد مواد قيد المراقبة.",
                        reply_markup=main_keyboard()
                    )
                else:
                    output = [
                        "📋 المواد قيد المراقبة:",
                        ""
                    ]

                    for i, line in enumerate(lines, 1):
                        title = (
                            course_meta.get(line, {}).get("title")
                            or COURSE_NAMES.get(line, "غير معروف")
                        )
                        output.append(
                            f"{i}. {title}"
                        )
                        output.append(
                            f"   🔢 {line}"
                        )

                    send_message(
                        callback_chat_id,
                        "\n".join(output),
                        reply_markup=main_keyboard()
                    )
                continue

            if callback_data == "show_status":
                lines = monitored_lines(target)

                if not lines:
                    send_message(
                        callback_chat_id,
                        "📭 لا توجد مواد قيد المراقبة.",
                        reply_markup=main_keyboard()
                    )
                else:
                    output = [
                        "📊 آخر حالة محفوظة:",
                        ""
                    ]

                    for line in lines:
                        meta = course_meta.get(line, {})
                        title = (
                            meta.get("title")
                            or COURSE_NAMES.get(line, "غير معروف")
                        )
                        output.append(
                            f"📚 {title}"
                        )
                        output.append(
                            f"رقم السطر: {line}"
                        )
                        output.append(
                            format_saved_status(
                                line,
                                states.get(line)
                            )
                        )
                        output.append("")

                    send_message(
                        callback_chat_id,
                        "\n".join(output),
                        reply_markup=main_keyboard()
                    )
                continue

            if callback_data == "show_help":
                send_message(
                    callback_chat_id,
                    help_text(),
                    reply_markup=main_keyboard()
                )
                continue

            if callback_data == "pause_monitor":
                target["paused"] = True
                target["mode"] = None
                target["ui_action"] = None
                changed = True
                send_message(
                    callback_chat_id,
                    "⏸️ تم إيقاف المراقبة مؤقتاً.",
                    reply_markup=main_keyboard()
                )
                continue

            if callback_data == "resume_monitor":
                if monitored_lines(target):
                    target["paused"] = False
                    changed = True
                    send_message(
                        callback_chat_id,
                        "▶️ تم استئناف المراقبة.",
                        reply_markup=main_keyboard()
                    )
                else:
                    send_message(
                        callback_chat_id,
                        "📭 لا توجد مواد قيد المراقبة.",
                        reply_markup=main_keyboard()
                    )
                continue

            if callback_data.startswith("update_status"):
                parts = callback_data.split(":", 1)
                line = target.get("line")
                if len(parts) == 2:
                    line = normalize_text(parts[1])

                key = (
                    str(callback_chat_id),
                    str(line or "")
                )

                if (
                    line
                    and line in monitored_lines(target)
                    and current_time - manual_update_times.get(key, 0) >= 30
                ):
                    manual_update_times[key] = current_time
                    add_force(
                        line,
                        callback_chat_id,
                        "status"
                    )
                    send_message(
                        callback_chat_id,
                        "🔄 جاري تحديث حالة المادة..."
                    )
                elif line:
                    send_message(
                        callback_chat_id,
                        "⏳ تم تحديث هذه المادة قبل قليل. انتظر قليلاً ثم جرّب مرة أخرى."
                    )
                else:
                    send_message(
                        callback_chat_id,
                        "📭 لا توجد مادة قيد المراقبة."
                    )
                continue

            continue

        message = update.get(
            "message",
            {}
        )

        chat = message.get(
            "chat",
            {}
        )

        chat_id = str(
            chat.get(
                "id",
                ""
            )
        )

        text = (
            message.get(
                "text"
            )
            or ""
        ).strip()

        if (
            not chat_id
            or not text
        ):
            continue

        target = get_user(
            users,
            chat_id
        )

        if not allow_user_action(chat_id):
            send_message(
                chat_id,
                "⏳ طلبات كثيرة خلال ثوانٍ قليلة. انتظر قليلاً ثم جرّب مرة أخرى."
            )
            continue

        command_match = re.match(
            r"^/([A-Za-z_]+)(?:@\w+)?(?:\s+(.+))?$",
            text
        )

        command = ""
        argument = ""

        if command_match:
            command = (
                command_match.group(1)
                or ""
            ).lower()

            argument = normalize_text(
                command_match.group(2)
                or ""
            )

        if command == "start":
            target["paused"] = False
            target["mode"] = None
            target["ui_action"] = None
            target["ui_faculty"] = None
            target["ui_department"] = None
            target["ui_page"] = 0

            count = len(
                monitored_lines(target)
            )

            send_message(
                chat_id,
                "👋 أهلاً بك في بوت مراقبة مواد JUST.\n\n"
                f"المواد المراقبة حالياً: {count}\n\n"
                "استخدم الأزرار بالأسفل للبدء.",
                reply_markup=main_keyboard()
            )

            changed = True

        elif command in (
            "help",
            "commands"
        ):
            send_message(
                chat_id,
                help_text(),
                reply_markup=main_keyboard()
            )

        elif command in (
            "settings",
            "alerts"
        ):
            target["mode"] = None
            target["ui_action"] = "settings"
            send_message(
                chat_id,
                settings_text(target),
                reply_markup=settings_keyboard(target)
            )
            changed = True

        elif command in (
            "dashboard",
            "dash"
        ):
            target["mode"] = None
            target["ui_action"] = "dashboard"
            send_message(
                chat_id,
                dashboard_text(users, course_meta),
                reply_markup=main_keyboard()
            )
            changed = True

        elif command in (
            "add",
            "watch"
        ):
            target["paused"] = False
            target["mode"] = None
            changed = True

            if argument:
                if known_course_line(argument):
                    line = normalize_text(argument)

                    if line in monitored_lines(target):
                        send_message(
                            chat_id,
                            f"ℹ️ المادة {COURSE_NAMES.get(line, line)} موجودة أصلاً في قائمة المراقبة.",
                            reply_markup=main_keyboard()
                        )
                    else:
                        add_line(
                            target,
                            line
                        )
                        add_force(
                            line,
                            chat_id,
                            "initial"
                        )
                        send_message(
                            chat_id,
                            f"✅ تمت إضافة {COURSE_NAMES.get(line, line)} للمراقبة.\n"
                            "جاري جلب حالتها الآن...",
                            reply_markup=main_keyboard()
                        )
                else:
                    send_message(
                        chat_id,
                        "❌ رقم السطر غير موجود ضمن المواد المدعومة.",
                        reply_markup=main_keyboard()
                    )
            else:
                target["ui_action"] = "add"
                target["ui_faculty"] = None
                target["ui_department"] = None
                target["ui_page"] = 0
                send_message(
                    chat_id,
                    add_menu_text(),
                    reply_markup=faculty_keyboard()
                )

        elif command in (
            "remove",
            "delete"
        ):
            target["paused"] = False
            target["mode"] = None
            changed = True

            if argument:
                if known_course_line(argument):
                    line = normalize_text(argument)

                    if line in monitored_lines(target):
                        remove_line(
                            target,
                            line
                        )

                        if not watchers_for_line(users, line):
                            states.pop(line, None)
                            missing_counts.pop(line, None)
                            course_meta.pop(line, None)

                        send_message(
                            chat_id,
                            f"✅ تم حذف {COURSE_NAMES.get(line, line)} من المراقبة.",
                            reply_markup=main_keyboard()
                        )
                    else:
                        send_message(
                            chat_id,
                            "ℹ️ المادة غير موجودة في قائمة المراقبة.",
                            reply_markup=main_keyboard()
                        )
                else:
                    send_message(
                        chat_id,
                        "❌ رقم السطر غير موجود ضمن المواد المدعومة.",
                        reply_markup=main_keyboard()
                    )
            else:
                lines = monitored_lines(target)
                target["ui_action"] = "remove"
                target["ui_page"] = 0

                if not lines:
                    send_message(
                        chat_id,
                        "📭 لا توجد مواد قيد المراقبة.\n\nأضف مادة أولاً.",
                        reply_markup=main_keyboard()
                    )
                else:
                    send_message(
                        chat_id,
                        remove_menu_text(lines, 0),
                        reply_markup=remove_keyboard(lines, 0)
                    )

        elif command in (
            "list",
            "courses",
            "watching"
        ):
            lines = monitored_lines(target)

            if not lines:
                send_message(
                    chat_id,
                    "📭 لا توجد مواد قيد المراقبة."
                )
            else:
                output = [
                    "📋 المواد قيد المراقبة:",
                    ""
                ]

                for index, line in enumerate(lines, 1):
                    meta = course_meta.get(
                        line,
                        {}
                    )

                    title = (
                        meta.get("title")
                        or "اسم المادة غير معروف بعد"
                    )

                    output.append(
                        f"{index}. {title}"
                    )

                    output.append(
                        f"   رقم السطر: {line}"
                    )

                send_message(
                    chat_id,
                    "\n".join(output),
                    reply_markup=main_keyboard()
                )

            target["mode"] = None
            changed = True

        elif command == "status":
            lines = monitored_lines(target)

            if not lines:
                send_message(
                    chat_id,
                    "📭 لا توجد مواد قيد المراقبة."
                )
            else:
                output = [
                    "📊 آخر حالة محفوظة:",
                    ""
                ]

                for line in lines:
                    meta = course_meta.get(
                        line,
                        {}
                    )

                    title = (
                        meta.get("title")
                        or "غير معروف"
                    )

                    output.append(
                        f"📚 {title}"
                    )

                    output.append(
                        f"رقم السطر: {line}"
                    )

                    output.append(
                        format_saved_status(
                            line,
                            states.get(line)
                        )
                    )

                    output.append("")

                send_message(
                    chat_id,
                    "\n".join(output),
                    reply_markup=status_keyboard(
                        target.get("line")
                    )
                )

        elif command in (
            "update",
            "refresh"
        ):
            lines = monitored_lines(target)

            if argument:
                if not valid_line(argument):
                    send_message(
                        chat_id,
                        "رقم السطر غير صحيح."
                    )
                elif argument not in lines:
                    send_message(
                        chat_id,
                        "هذه المادة غير موجودة في قائمة المراقبة."
                    )
                else:
                    key = (
                        str(chat_id),
                        str(argument)
                    )

                    if current_time - manual_update_times.get(key, 0) < 30:
                        send_message(
                            chat_id,
                            "⏳ تم تحديث هذه المادة قبل قليل."
                        )
                    else:
                        manual_update_times[key] = current_time
                        add_force(
                            argument,
                            chat_id,
                            "status"
                        )
                        send_message(
                            chat_id,
                            f"🔄 جاري تحديث رقم السطر {argument}..."
                        )

            elif lines:
                available = []

                for line in lines:
                    key = (
                        str(chat_id),
                        str(line)
                    )

                    if current_time - manual_update_times.get(key, 0) >= 30:
                        manual_update_times[key] = current_time
                        available.append(line)
                        add_force(
                            line,
                            chat_id,
                            "status"
                        )

                if available:
                    send_message(
                        chat_id,
                        "🔄 جاري تحديث حالة جميع المواد..."
                    )
                else:
                    send_message(
                        chat_id,
                        "⏳ تم تحديث المواد قبل قليل. "
                        "انتظر قليلاً ثم جرّب مرة أخرى."
                    )

            else:
                send_message(
                    chat_id,
                    "لا توجد مواد قيد المراقبة."
                )

        elif command in (
            "stop",
            "pause"
        ):
            target["paused"] = True
            target["mode"] = None
            changed = True

            send_message(
                chat_id,
                "⏸️ تم إيقاف المراقبة مؤقتاً.\n\n"
                "استخدم /resume لاستئنافها."
            )

        elif command in (
            "resume",
            "startmonitor"
        ):
            if monitored_lines(target):
                target["paused"] = False
                changed = True

                send_message(
                    chat_id,
                    "▶️ تم استئناف المراقبة."
                )
            else:
                send_message(
                    chat_id,
                    "لا توجد مواد قيد المراقبة.\n"
                    "استخدم /add أولاً."
                )

        elif command in (
            "end",
            "endmonitor"
        ):
            old_lines = list(
                monitored_lines(target)
            )

            target["lines"] = []
            target["line"] = None
            target["mode"] = None
            target["paused"] = True
            target["ui_action"] = None
            target["ui_faculty"] = None
            target["ui_department"] = None
            target["ui_page"] = 0

            for line in old_lines:
                if not watchers_for_line(users, line):
                    states.pop(line, None)
                    missing_counts.pop(line, None)
                    course_meta.pop(line, None)

            changed = True

            send_message(
                chat_id,
                "🛑 تم إنهاء المراقبة وحذف جميع المواد من القائمة.\n\n"
                "يمكنك استخدام /start للبدء من جديد."
            )

        elif valid_line(text):
            line = normalize_text(
                text
            )

            mode = target.get(
                "mode"
            )

            if mode == "remove":
                if line in monitored_lines(target):
                    remove_line(
                        target,
                        line
                    )

                    if not watchers_for_line(users, line):
                        states.pop(line, None)
                        missing_counts.pop(line, None)
                        course_meta.pop(line, None)

                    changed = True

                    send_message(
                        chat_id,
                        f"🗑️ تم حذف المادة {line} من المراقبة.",
                        reply_markup=main_keyboard()
                    )
                else:
                    send_message(
                        chat_id,
                        f"رقم السطر {line} غير موجود في قائمة المراقبة."
                    )

                target["mode"] = None

            else:
                if (
                    mode == "add"
                    or not monitored_lines(target)
                ):
                    if not known_course_line(line):
                        send_message(
                            chat_id,
                            "رقم السطر غير موجود ضمن المواد المدعومة."
                        )
                        continue

                    add_line(
                        target,
                        line
                    )

                    add_force(
                        line,
                        chat_id,
                        "initial"
                    )

                    changed = True

                    send_message(
                        chat_id,
                        f"➕ تمت إضافة رقم السطر {line} للمراقبة.\n"
                        "جاري جلب اسم المادة والشعب والحالة...",
                        reply_markup=main_keyboard()
                    )
                else:
                    send_message(
                        chat_id,
                        "استخدم /add لإضافة مادة جديدة، "
                        "أو /remove لحذف مادة."
                    )

        elif text.startswith("/"):
            send_message(
                chat_id,
                "❓ أمر غير معروف.\n\n"
                "استخدم /help لرؤية الأوامر."
            )

        else:
            if target.get("mode") == "add":
                send_message(
                    chat_id,
                    "استخدم /add أو زر ➕ إضافة مادة لاختيار الكلية ثم القسم ثم المادة.",
                    reply_markup=main_keyboard()
                )
            elif target.get("mode") == "remove":
                send_message(
                    chat_id,
                    "استخدم /remove أو زر 🗑️ حذف مادة لاختيار مادة من القائمة.",
                    reply_markup=main_keyboard()
                )

    if changed:
        save_users(users_data)

    return (
        users_data,
        states,
        missing_counts,
        course_meta,
        force_requests
    )


def open_browser():
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch_persistent_context(
        PROFILE_FOLDER,
        headless=False,
        channel="chrome"
    )

    page = (
        browser.pages[0]
        if browser.pages
        else browser.new_page()
    )

    page.set_default_timeout(
        30000
    )

    page.goto(
        SITE_URL,
        wait_until="domcontentloaded"
    )

    page.wait_for_timeout(
        3000
    )

    page.select_option(
        "#ctl00_contentPH_ddlFaculty",
        FACULTY_VALUE
    )

    page.wait_for_timeout(
        2000
    )

    page.select_option(
        "#ctl00_contentPH_ddlDept",
        INITIAL_DEPT_VALUE
    )

    page.wait_for_timeout(
        2000
    )

    ensure_manual_verification(
        page
    )

    return (
        playwright,
        browser,
        page
    )


def ensure_manual_verification(page):
    locator = page.locator(
        "input[name='cf-turnstile-response']"
    )

    if locator.count() == 0:
        return

    try:
        value = locator.first.input_value()

        if value:
            return
    except Exception:
        pass

    page.bring_to_front()

    print("=" * 70)
    print(
        "Cloudflare verification may be required."
    )
    print(
        "Solve the verification manually in the browser."
    )
    print(
        "When finished, press Enter here."
    )
    print("=" * 70)

    try:
        input("اضغط Enter بعد إكمال التحقق اليدوي... ")
    except EOFError:
        pass


def save_debug(page):
    try:
        DEBUG_HTML_FILE.write_text(
            page.content(),
            encoding="utf-8"
        )
    except Exception:
        pass

    try:
        page.screenshot(
            path=str(
                DEBUG_SCREENSHOT_FILE
            ),
            full_page=True
        )
    except Exception:
        pass


def page_health_ok(page):
    try:
        if page.is_closed():
            return False

        page.locator("body").count()
        return True
    except Exception:
        return False


def recover_page(page, faculty_value=None, dept_value=None):
    global DEPARTMENT_CACHE

    try:
        context = page.context
    except Exception:
        return page, False

    try:
        for existing in context.pages:
            if not existing.is_closed():
                try:
                    existing.locator("body").count()
                    if existing.url:
                        page = existing
                        break
                except Exception:
                    continue
        else:
            page = context.new_page()

        page.set_default_timeout(30000)
        page.goto(
            SITE_URL,
            wait_until="domcontentloaded"
        )
        page.wait_for_timeout(3000)

        if faculty_value is not None:
            select_faculty(page, faculty_value)

        if dept_value is not None and str(dept_value) != "-1":
            select_department(page, dept_value)

        ensure_manual_verification(page)
        DEPARTMENT_CACHE.clear()
        RUNTIME_STATS["total_recoveries"] += 1
        print("Browser page recovered successfully.")
        return page, True

    except Exception as e:
        print("Browser page recovery failed:", repr(e))
        return page, False


def select_faculty(page, faculty_value):
    current = None

    try:
        current = page.locator(
            "#ctl00_contentPH_ddlFaculty"
        ).input_value()
    except Exception:
        pass

    if str(current or "") == str(faculty_value):
        return

    page.select_option(
        "#ctl00_contentPH_ddlFaculty",
        str(faculty_value)
    )

    page.wait_for_timeout(
        2000
    )


def select_department(page, dept_value):
    current = None

    try:
        current = page.locator(
            "#ctl00_contentPH_ddlDept"
        ).input_value()
    except Exception:
        pass

    if str(current or "") == str(dept_value):
        return

    page.select_option(
        "#ctl00_contentPH_ddlDept",
        str(dept_value)
    )

    page.wait_for_timeout(
        2000
    )


def select_location(page, faculty_value, dept_value):
    select_faculty(
        page,
        faculty_value
    )

    if str(dept_value) == "-1":
        return

    select_department(
        page,
        dept_value
    )


def fetch_schedule_html(page):
    page.click(
        "#ctl00_contentPH_btnSubmit"
    )

    page.wait_for_timeout(
        5000
    )

    html = page.content()

    save_debug(
        page
    )

    page_low = html.lower()

    rate_limit_markers = [
        "too many requests",
        "429",
        "rate limit",
        "requests are too frequent"
    ]

    if any(
        marker in page_low
        for marker in rate_limit_markers
    ):
        raise RateLimitedError(
            "JUST returned a rate-limit response."
        )

    verification_markers = [
        "لم يتم التأكد من هوية المستخدم",
        "identity could not be verified",
        "identity verification"
    ]

    if any(
        marker.lower() in page_low
        for marker in verification_markers
    ):
        raise VerificationError(
            "JUST rejected the verification/session."
        )

    return html


def parse_fetched_course(html, line):
    course = parse_course(
        html,
        line
    )

    if course is None:
        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        full_text = normalize_text(
            soup.get_text(
                " ",
                strip=True
            )
        )

        row_numbers = sorted(
            set(
                re.findall(
                    r"\b\d{7,10}\b",
                    full_text
                )
            )
        )

        raise RuntimeError(
            f"Could not find row number {line}. "
            f"Numbers found: {row_numbers[:50]}. "
            f"Debug files: {DEBUG_HTML_FILE.resolve()} "
            f"and {DEBUG_SCREENSHOT_FILE.resolve()}"
        )

    if not course["sections"]:
        raise RuntimeError(
            "No sections were parsed. "
            "Skipping this check."
        )

    return course


def fetch_course(page, line):
    html = fetch_schedule_html(
        page
    )

    return parse_fetched_course(
        html,
        line
    )


def build_next_check_time():
    return (
        time.time()
        + SITE_CHECK_INTERVAL_SECONDS
        + random.uniform(
            0,
            CHECK_JITTER_SECONDS
        )
    )


def monitor_loop(
    users_data,
    states,
    missing_counts,
    course_meta,
    page
):
    next_site_check = 0
    check_count = 0
    manual_update_times = {}
    rate_limit_refresh_pending = False

    while True:
        try:
            if not page_health_ok(page):
                page, recovered = recover_page(page)
                if not recovered:
                    time.sleep(ERROR_BACKOFF_SECONDS)
                    continue

            (
                users_data,
                states,
                missing_counts,
                course_meta,
                force_requests
            ) = handle_commands(
                users_data,
                states,
                missing_counts,
                course_meta,
                manual_update_times
            )

            users = users_data.get(
                "users",
                {}
            )

            if not users:
                time.sleep(1)
                continue

            force_lines = []
            for request in force_requests:
                line = normalize_text(
                    request.get("line")
                )
                if line and line not in force_lines:
                    force_lines.append(line)

            auto_due = (
                bool(active_monitored_lines(users))
                and time.time() >= next_site_check
            )

            if force_lines:
                lines_to_check = list(
                    dict.fromkeys(force_lines)
                )
                is_forced_cycle = True
            elif auto_due:
                lines_to_check = active_monitored_lines(users)
                is_forced_cycle = False
            else:
                lines_to_check = []
                is_forced_cycle = False

            if not lines_to_check:
                time.sleep(1)
                continue

            if auto_due and rate_limit_refresh_pending:
                print(
                    "Rate-limit wait finished. Refreshing JUST page..."
                )

                try:
                    page.reload(
                        wait_until="domcontentloaded"
                    )

                    page.wait_for_timeout(
                        3000
                    )

                    save_debug(
                        page
                    )

                    DEPARTMENT_CACHE.clear()
                    rate_limit_refresh_pending = False

                    print(
                        "JUST page refreshed successfully."
                    )

                except Exception as e:
                    print(
                        "Page refresh after rate limit failed:",
                        repr(e)
                    )

                    next_site_check = (
                        time.time()
                        + ERROR_BACKOFF_SECONDS
                    )

                    time.sleep(1)
                    continue

            groups = group_lines_by_department(
                lines_to_check
            )

            unknown_lines = [
                line
                for line in lines_to_check
                if not department_for_line(line)
            ]

            for unknown_line in unknown_lines:
                print(
                    f"Skipping unsupported row {unknown_line}: "
                    "no department mapping."
                )

            department_groups = list(
                groups.items()
            )

            for group_index, ((faculty_value, dept_value), dept_lines) in enumerate(
                department_groups
            ):
                active_lines = [
                    line
                    for line in dept_lines
                    if line in lines_to_check
                ]

                if not active_lines:
                    continue

                print(
                    f"Preparing faculty {faculty_value} / department {dept_value} "
                    f"({department_name(dept_value)}) | "
                    f"{len(active_lines)} course(s)"
                )

                try:
                    select_location(
                        page,
                        faculty_value,
                        dept_value
                    )

                    batch_html = get_cached_department_html(
                        faculty_value,
                        dept_value
                    )

                    if batch_html is None:
                        batch_html = fetch_schedule_html(
                            page
                        )
                        cache_department_html(
                            faculty_value,
                            dept_value,
                            batch_html
                        )
                    else:
                        print(
                            f"Using department cache: faculty {faculty_value} / department {dept_value}"
                        )

                    RUNTIME_STATS["total_department_batches"] += 1

                except VerificationError:
                    print(
                        "Verification required. "
                        "Waiting for manual solve..."
                    )

                    page.bring_to_front()

                    ensure_manual_verification(
                        page
                    )

                    batch_html = fetch_schedule_html(
                        page
                    )
                    cache_department_html(
                        faculty_value,
                        dept_value,
                        batch_html
                    )
                    RUNTIME_STATS["total_department_batches"] += 1

                for watched_line in active_lines:
                    check_count += 1
                    RUNTIME_STATS["total_site_checks"] += 1

                    print(
                        f"Site check #{check_count} | "
                        f"Row: {watched_line} | "
                        f"Faculty: {faculty_value} | "
                        f"Department: {dept_value} | "
                        "shared page snapshot"
                    )

                    try:
                        course = parse_fetched_course(
                            batch_html,
                            watched_line
                        )

                    except Exception as e:
                        print(
                            f"Course parse error for row "
                            f"{watched_line}: {e!r}"
                        )
                        continue

                    course_meta[watched_line] = {
                        "title": course.get(
                            "title",
                            ""
                        ),
                        "code": course.get(
                            "code",
                            ""
                        ),
                        "hours": course.get(
                            "hours",
                            ""
                        ),
                        "faculty": faculty_value,
                        "department": dept_value,
                        "department_name": department_name(
                            dept_value
                        )
                    }

                    new_snapshot = snapshot(
                        course
                    )

                    line_initial_requesters = [
                        str(r["chat_id"])
                        for r in force_requests
                        if (
                            normalize_text(r.get("line")) == watched_line
                            and r.get("mode") == "initial"
                        )
                    ]

                    line_status_requesters = [
                        str(r["chat_id"])
                        for r in force_requests
                        if (
                            normalize_text(r.get("line")) == watched_line
                            and r.get("mode") == "status"
                        )
                    ]

                    line_has_manual_request = bool(
                        line_initial_requesters
                        or line_status_requesters
                    )

                    if line_status_requesters and not line_initial_requesters:
                        for chat_id in dict.fromkeys(
                            line_status_requesters
                        ):
                            send_message(
                                chat_id,
                                format_initial_status(
                                    course
                                ),
                                reply_markup=status_keyboard(
                                    watched_line
                                )
                            )
                        continue

                    if line_initial_requesters:
                        old_snapshot = states.get(
                            watched_line
                        )

                        if old_snapshot is None:
                            states[watched_line] = (
                                new_snapshot
                            )

                            missing_counts[watched_line] = {}

                            initial_recipients = watchers_for_line(
                                users,
                                watched_line,
                                include_paused=True
                            )
                        else:
                            initial_recipients = list(
                                dict.fromkeys(
                                    line_initial_requesters
                                )
                            )

                        for chat_id in dict.fromkeys(
                            initial_recipients
                        ):
                            send_message(
                                chat_id,
                                format_initial_status(
                                    course
                                ),
                                reply_markup=status_keyboard(
                                    watched_line
                                )
                            )

                        continue

                    old_snapshot = states.get(
                        watched_line
                    )

                    if old_snapshot is None:
                        states[watched_line] = (
                            new_snapshot
                        )

                        missing_counts[watched_line] = {}

                        recipients = watchers_for_line(
                            users,
                            watched_line
                        )

                        for chat_id in recipients:
                            send_message(
                                chat_id,
                                format_initial_status(
                                    course
                                ),
                                reply_markup=status_keyboard(
                                    watched_line
                                )
                            )

                    else:
                        events = compare_course(
                            old_snapshot,
                            new_snapshot
                        )

                        counts = missing_counts.setdefault(
                            watched_line,
                            {}
                        )

                        confirmed_removed = set()
                        real_events = []

                        for event in events:
                            if (
                                event["type"]
                                != "removed_section"
                            ):
                                real_events.append(
                                    event
                                )
                                continue

                            section = event[
                                "section"
                            ]

                            counts[section] = (
                                counts.get(
                                    section,
                                    0
                                ) + 1
                            )

                            if (
                                counts[section]
                                >= REMOVAL_CONFIRMATION_CHECKS
                            ):
                                confirmed_removed.add(
                                    section
                                )

                                real_events.append(
                                    event
                                )

                        current_sections = set(
                            new_snapshot.keys()
                        )

                        for section in list(
                            counts.keys()
                        ):
                            if section in current_sections:
                                counts.pop(
                                    section,
                                    None
                                )

                        stored_snapshot = dict(
                            new_snapshot
                        )

                        for (
                            section,
                            old_data
                        ) in old_snapshot.items():
                            if section not in new_snapshot:
                                if (
                                    section
                                    not in confirmed_removed
                                ):
                                    stored_snapshot[
                                        section
                                    ] = old_data

                        recipients = watchers_for_line(
                            users,
                            watched_line
                        )

                        for event in real_events:
                            message = format_event(
                                course,
                                event
                            )

                            if message:
                                event_recipients = [
                                    chat_id
                                    for chat_id in recipients
                                    if event_allowed_for_user(
                                        users.get(str(chat_id), {}),
                                        event
                                    )
                                ]

                                for chat_id in event_recipients:
                                    send_message(
                                        chat_id,
                                        message
                                    )
                                if event_recipients:
                                    time.sleep(1)

                        states[watched_line] = (
                            stored_snapshot
                        )

                save_json(
                    STATE_FILE,
                    states
                )

                save_json(
                    Path("course_metadata.json"),
                    course_meta
                )

                if group_index < len(department_groups) - 1:
                    print(
                        f"Waiting {DEPARTMENT_CHECK_DELAY_SECONDS} seconds before next department check..."
                    )
                    time.sleep(
                        DEPARTMENT_CHECK_DELAY_SECONDS
                    )

            save_json(
                STATE_FILE,
                states
            )

            save_json(
                Path("course_metadata.json"),
                course_meta
            )

            save_users(
                users_data
            )

            RUNTIME_STATS["last_success_at"] = time.time()
            RUNTIME_STATS["last_error"] = ""

            if auto_due:
                next_site_check = build_next_check_time()

        except RateLimitedError as e:
            print(
                "RATE LIMIT:",
                e
            )

            RUNTIME_STATS["total_rate_limits"] += 1
            RUNTIME_STATS["last_error"] = "Rate Limit"
            DEPARTMENT_CACHE.clear()

            next_site_check = (
                time.time()
                + RATE_LIMIT_BACKOFF_SECONDS
            )

            rate_limit_refresh_pending = True

            notified = set()
            for line in active_monitored_lines(
                users_data.get("users", {})
            ):
                for chat_id in watchers_for_line(
                    users_data.get("users", {}),
                    line
                ):
                    if chat_id in notified:
                        continue
                    notified.add(chat_id)
                    send_message(
                        chat_id,
                        "⚠️ موقع JUST طلب تهدئة الاتصالات.\n\n"
                        f"رح أنتظر "
                        f"{RATE_LIMIT_BACKOFF_SECONDS // 60} "
                        "دقائق قبل الفحص القادم."
                    )

        except VerificationError:
            print(
                "Verification is still required."
            )

            RUNTIME_STATS["last_error"] = "Verification required"

            next_site_check = (
                time.time()
                + ERROR_BACKOFF_SECONDS
            )

        except Exception as e:
            print(
                "Monitor error:",
                repr(e)
            )

            RUNTIME_STATS["last_error"] = repr(e)[:300]

            try:
                page, recovered = recover_page(page)
                if recovered:
                    next_site_check = time.time()
                else:
                    next_site_check = time.time() + ERROR_BACKOFF_SECONDS
            except Exception:
                next_site_check = (
                    time.time()
                    + SITE_CHECK_INTERVAL_SECONDS
                )

        time.sleep(1)


def run():
    print("=" * 70)
    print("JUST Course Schedule Monitor")
    print("=" * 70)

    if not check_telegram():
        input(
            "\nTelegram connection failed. "
            "Press Enter to close..."
        )
        return

    users_data = load_users()

    states = load_json(
        STATE_FILE,
        {}
    )

    missing_counts = {}

    course_meta_file = Path(
        "course_metadata.json"
    )

    course_meta = load_json(
        course_meta_file,
        {}
    )

    monitored = set(
        all_monitored_lines(
            users_data.get("users", {})
        )
    )

    for line in list(
        course_meta.keys()
    ):
        if line not in monitored:
            course_meta.pop(
                line,
                None
            )

    save_json(
        course_meta_file,
        course_meta
    )

    save_users(
        users_data
    )

    playwright = None
    browser = None

    try:
        (
            playwright,
            browser,
            page
        ) = open_browser()

        print(
            "\nBOT IS RUNNING"
        )

        print(
            "Open Telegram and send /start"
        )

        monitor_loop(
            users_data,
            states,
            missing_counts,
            course_meta,
            page
        )

    except KeyboardInterrupt:
        print(
            "\nStopping..."
        )

    except Exception as e:
        print(
            "Fatal error:",
            repr(e)
        )

        input(
            "\nPress Enter to close..."
        )

    finally:
        if browser:
            try:
                browser.close()
            except Exception:
                pass

        if playwright:
            try:
                playwright.stop()
            except Exception:
                pass


if __name__ == "__main__":
    run()

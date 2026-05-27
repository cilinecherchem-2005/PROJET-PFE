// Sidebar + i18n + Dark mode for JADARA RH (Yassir-RH)

(function(){
  const body = document.body;
  const langSelect = document.getElementById('langSelect');
  const themeToggle = document.getElementById('themeToggle');
  const rtlLanguages = new Set(['ar','ar_AR','ar-EG','ar-DZ','العربية']);

  const storageThemeKey = 'theme';
  const storageLangKey = 'langue';

  function setRTL(lang){
    const isRTL = rtlLanguages.has(lang) || lang.startsWith('ar');
    document.body.dir = isRTL ? 'rtl' : 'ltr';
  }

  function applyDarkMode(isDark){
    if(isDark){
      body.classList.add('dark-mode');
    }else{
      body.classList.remove('dark-mode');
    }
  }

  const dict = {
    fr: {

      page_title: "Recrutez plus vite avec l'IA",
      page_subtitle: 'Publiez des offres, uploadez vos CV et automatisez le matching intelligent.',
      card_offer: 'Publiez une offre',
      card_upload: 'Uploadez les CV',
      card_match: 'Matching intelligent',
      nav_dashboard: 'Dashboard',
      nav_offres: 'Offres',
      nav_upload: 'Upload CV',
      nav_candidats: 'Candidats',
      nav_assistant: 'Assistant IA',
      btn_match: 'Matcher →',
      btn_new_offer: '+ Nouvelle offre',
      upload_title: 'Analyser un CV',
      upload_cta: 'Analyser le CV',
      candidates_title: 'CVs analysés',
    },
    en: {
      page_title: 'Recruit faster with AI',
      page_subtitle: 'Publish jobs, upload CVs, and automate intelligent matching.',
      card_offer: 'Publish a job',
      card_upload: 'Upload CVs',
      card_match: 'Intelligent matching',
      nav_dashboard: 'Dashboard',
      nav_offres: 'Jobs',
      nav_upload: 'Upload CV',
      nav_candidats: 'Candidates',
      nav_assistant: 'AI Assistant',
      btn_match: 'Match →',
      btn_new_offer: '+ New job',
      upload_title: 'Analyze a CV',
      upload_cta: 'Analyze the CV',
      candidates_title: 'Analyzed CVs',
    },
    ar: {
      page_title: 'سرّع التوظيف بالذكاء الاصطناعي',
      page_subtitle: 'انشر الوظائف، ارفع السير الذاتية، وأتمتة المطابقة الذكية.',
      card_offer: 'انشر وظيفة',
      card_upload: 'ارفع السيرة الذاتية',
      card_match: 'مطابقة ذكية',
      nav_dashboard: 'لوحة التحكم',
      nav_offres: 'الوظائف',
      nav_upload: 'رفع السيرة',
      nav_candidats: 'المرشحون',
      nav_assistant: 'مساعد الذكاء',
      btn_match: 'مطابقة →',
      btn_new_offer: '+ وظيفة جديدة',
      upload_title: 'تحليل السيرة',
      upload_cta: 'حلّل السيرة',
      candidates_title: 'السير الذاتية المحللة',
    }
  };

  function updateTexts(lang){
    const t = dict[lang] || dict.fr;
    document.querySelectorAll('[data-i18n-key]').forEach(el=>{
      const key = el.getAttribute('data-i18n-key');
      if(t[key]) el.textContent = t[key];
    });
  }

  // init
  const storedLang = localStorage.getItem(storageLangKey) || 'fr';
  const storedTheme = localStorage.getItem(storageThemeKey) || 'light';

  if(langSelect){
    langSelect.value = storedLang;
    updateTexts(storedLang);
    setRTL(storedLang);

    langSelect.addEventListener('change', (e)=>{
      const lang = e.target.value;
      localStorage.setItem(storageLangKey, lang);
      updateTexts(lang);
      setRTL(lang);
    });
  }

  // Toggle switch
  if(themeToggle){
    const isDark = storedTheme === 'dark';
    applyDarkMode(isDark);

    themeToggle.addEventListener('click', ()=>{
      const nextDark = !body.classList.contains('dark-mode');
      applyDarkMode(nextDark);
      localStorage.setItem(storageThemeKey, nextDark ? 'dark' : 'light');
    });
  }

})();


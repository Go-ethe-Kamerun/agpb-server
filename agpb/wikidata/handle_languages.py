def getLanguages():
    languages = [
      {
        'lang_code': 'afr',
        'wd_id': 'Q14196',
        'language': 'Afrikaans'
      },
      {
        'lang_code': 'bag',
        'wd_id': 'Q36621',
        'language': 'Tuki'
      },
      {
        'lang_code': 'bas',
        'wd_id': 'Q33093',
        'language': 'Basaa'
      },
      {
        'lang_code': 'bax',
        'wd_id': None,
        'language': 'Bamun'
      },
      {
        'lang_code': 'bbj',
        'wd_id': 'Q35271',
        'language': 'Ghamála'
      },
      {
        'lang_code': 'bfd',
        'wd_id': 'Q34888',
        'language': 'Bafut'
      },
      {
        'lang_code': 'bkc',
        'wd_id': 'Q2880165',
        'language': 'Baka'
      },
      {
        'lang_code': 'bkh',
        'wd_id': 'Q34866',
        'language': 'Bakoko'
      },
      {
        'lang_code': 'bkm',
        'wd_id': 'Q1656595',
        'language': 'Kom'
      },
      {
        'lang_code': 'byv',
        'wd_id': 'Q36019',
        'language': 'Medumba'
      },
      {
        'lang_code': 'bzk',
        'wd_id': 'Q107695495',
        'language': 'Mka\'a'
      },
      {
        'lang_code': 'de',
        'wd_id': 'Q188',
        'language': 'German'
      },
      {
        'lang_code': 'dua',
        'wd_id': 'Q33013',
        'language': 'Duala'
      },
      {
        'lang_code': 'en',
        'wd_id': 'Q1860',
        'language': 'English'
      },
      {
        'lang_code': 'eto',
        'wd_id': 'Q35317',
        'language': 'Eton'
      },
      {
        'lang_code': 'etu',
        'wd_id': 'Q35296',
        'language': 'Ejagham'
      },
      {
        'lang_code': 'ewe',
        'wd_id': 'Q30005',
        'language': 'Éwé'
      },
      {
        'lang_code': 'ewo',
        'wd_id': 'Q35459',
        'language': 'Ewondo'
      },
      {
        'lang_code': 'fr',
        'wd_id': 'Q150',
        'language': 'Français'
      },
      {
        'lang_code': 'fmp',
        'wd_id': 'Q35276',
        'language': 'Fe\'fe\''
      },
      {
        'lang_code': 'ful',
        'wd_id': 'Q33454',
        'language': 'Fulfulde'
      },
      {
        'lang_code': 'fuc',
        'wd_id': 'Q1420205',
        'language': 'Pulaar'
      },
      {
        'lang_code': 'gba',
        'wd_id': 'Q3099986',
        'language': 'Gbaya'
      },
      {
        'lang_code': 'hau',
        'wd_id': 'Q56475',
        'language': 'Hausa'
      },
      {
        'lang_code': 'her',
        'wd_id': 'Q33315',
        'language': 'Otjiherero'
      },
      {
        'lang_code': 'ibo',
        'wd_id': 'Q33578',
        'language': 'Igbo'
      },
      {
        'lang_code': 'isu',
        'wd_id': 'Q6089423',
        'language': 'Isu'
      },
      {
        'lang_code': 'ker',
        'wd_id': 'Q56251',
        'language': 'Kera'
      },
      {
        'lang_code': 'ksf',
        'wd_id': 'Q34930',
        'language': 'Bafia'
      },
      {
        'lang_code': 'kua',
        'wd_id': 'Q1405077',
        'language': 'Oshikwanyama'
      },
      {
        'lang_code': 'kwn',
        'wd_id': 'Q36334',
        'language': 'Rukwangali'
      },
      {
        'lang_code': 'lem',
        'wd_id': 'Q13479983',
        'language': 'Nomaande'
      },
      {
        'lang_code': 'lin',
        'wd_id': 'Q36217',
        'language': 'Lingala'
      },
      {
        'lang_code': 'lns',
        'wd_id': 'Q35788',
        'language': 'Nso'
      },
      {
        'lang_code': 'mca',
        'wd_id': 'Q3281043',
        'language': 'Maká'
      },
      {
        'lang_code': 'mlg',
        'wd_id': 'Q7930',
        'language': 'Malagasy'
      },
      {
        'lang_code': 'mua',
        'wd_id': 'Q36032',
        'language': 'Mundang'
      },
      {
        'lang_code': 'naq',
        'wd_id': 'Q13301',
        'language': 'KhoeKhoegowab'
      },
      {
        'lang_code': 'ndo',
        'wd_id': 'Q33900',
        'language': 'Oshindonga'
      },
      {
        'lang_code': 'nla',
        'wd_id': 'Q107695546',
        'language': 'Ngombala'
      },
      {
        'lang_code': 'nmg',
        'wd_id': 'Q34098',
        'language': 'Kwasio'
      },
      {
        'lang_code': 'nnh',
        'wd_id': 'Q36286',
        'language': 'Ngiemboon'
      },
      {
        'lang_code': 'nso',
        'wd_id': 'Q33890',
        'language': 'Sepedi'
      },
      {
        'lang_code': 'swa',
        'wd_id': 'Q7838',
        'language': 'Kiswahili'
      },
      {
        'lang_code': 'tsn',
        'wd_id': 'Q34137',
        'language': 'Setswana'
      },
      {
        'lang_code': 'tvu',
        'wd_id': 'Q36632',
        'language': 'Tunen'
      },
      {
        'lang_code': 'twi',
        'wd_id': 'Q36850',
        'language': 'Twi'
      },
      {
        'lang_code': 'vut',
        'wd_id': 'Q36897',
        'language': 'Vute'
      },
      {
        'lang_code': 'wes',
        'wd_id': 'Q33831',
        'language': 'Pidgin'
      },
      {
        'lang_code': 'wol',
        'wd_id': 'Q34257',
        'language': 'Wolof'
      },
      {
        'lang_code': 'xho',
        'wd_id': 'Q13218',
        'language': 'isiXhosa'
      },
      {
        'lang_code': 'yas',
        'wd_id': 'Q36358',
        'language': 'Nugunu'
      },
      {
        'lang_code': 'yat',
        'wd_id': 'Q8048020',
        'language': 'Yambeta'
      },
      {
        'lang_code': 'yav',
        'wd_id': 'Q8048020',
        'language': 'Yangben'
      },
      {
        'lang_code': 'ybb',
        'wd_id': 'Q36917',
        'language': 'Yemba'
      },
      {
        'lang_code': 'yor',
        'wd_id': 'Q34311',
        'language': 'Yoruba'
      },
      {
        'lang_code': 'zul',
        'wd_id': 'Q10179',
        'language': 'isiZulu'
      }
    ]

    return languages
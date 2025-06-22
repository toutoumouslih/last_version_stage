from decimal import Decimal

DEMOGRAPHIC_DATA = {
    'MR01': {  # Hodh Chargui
        'population': 512957,
        'male': Decimal('48.2'),
        'female': Decimal('51.8'),
        'urban': Decimal('0'),
        'rural': Decimal('0'),
        'departments': {
            'MR011': {  # Amourj
                'population': 62147,
                'male': Decimal('47.8'),
                'female': Decimal('52.2'),
                'urban': Decimal('18.5'),
                'rural': Decimal('81.5')
            },
            'MR012': {  # Bassikounou
                'population': 118374,
                'male': Decimal('48.5'),
                'female': Decimal('51.5'),
                'urban': Decimal('21.2'),
                'rural': Decimal('78.8')
            },
            'MR013': {  # Djiguenni
                'population': 82073,
                'male': Decimal('47.9'),
                'female': Decimal('52.1'),
                'urban': Decimal('19.8'),
                'rural': Decimal('80.2')
            },
            'MR014': {  # Néma
                'population': 137889,
                'male': Decimal('48.4'),
                'female': Decimal('51.6'),
                'urban': Decimal('26.3'),
                'rural': Decimal('73.7')
            },
            'MR015': {  # Oualata
                'population': 11474,
                'male': Decimal('48.7'),
                'female': Decimal('51.3'),
                'urban': Decimal('24.5'),
                'rural': Decimal('75.5')
            }
        }
    },
    'MR02': {  # Hodh El Gharbi
        'population': 325991,
        'male': Decimal('48.5'),
        'female': Decimal('51.5'),
        'urban': Decimal('24.8'),
        'rural': Decimal('75.2'),
        'departments': {
            'MR021': {  # Aioun
                'population': 138421,
                'male': Decimal('48.7'),
                'female': Decimal('51.3'),
                'urban': Decimal('28.5'),
                'rural': Decimal('71.5')
            },
            'MR022': {  # Kobeni
                'population': 106324,
                'male': Decimal('48.3'),
                'female': Decimal('51.7'),
                'urban': Decimal('22.4'),
                'rural': Decimal('77.6')
            },
            'MR023': {  # Tamchekett
                'population': 81246,
                'male': Decimal('48.4'),
                'female': Decimal('51.6'),
                'urban': Decimal('21.5'),
                'rural': Decimal('78.5')
            }
        }
    },
    'MR03': {  # Assaba
        'population': 442486,
        'male': Decimal('48.6'),
        'female': Decimal('51.4'),
        'urban': Decimal('26.2'),
        'rural': Decimal('73.8'),
        'departments': {
            'MR031': {  # Barkéol
                'population': 89472,
                'male': Decimal('48.4'),
                'female': Decimal('51.6'),
                'urban': Decimal('23.8'),
                'rural': Decimal('76.2')
            },
            'MR032': {  # Boumdeid
                'population': 24563,
                'male': Decimal('48.7'),
                'female': Decimal('51.3'),
                'urban': Decimal('24.2'),
                'rural': Decimal('75.8')
            },
            'MR033': {  # Guerou
                'population': 118246,
                'male': Decimal('48.8'),
                'female': Decimal('51.2'),
                'urban': Decimal('27.5'),
                'rural': Decimal('72.5')
            },
            'MR034': {  # Kiffa
                'population': 210205,
                'male': Decimal('48.6'),
                'female': Decimal('51.4'),
                'urban': Decimal('26.8'),
                'rural': Decimal('73.2')
            }
        }
    },
    'MR04': {  # Gorgol
        'population': 403384,
        'male': Decimal('48.4'),
        'female': Decimal('51.6'),
        'urban': Decimal('25.8'),
        'rural': Decimal('74.2'),
        'departments': {
            'MR041': {  # Kaédi
                'population': 145218,
                'male': Decimal('48.6'),
                'female': Decimal('51.4'),
                'urban': Decimal('28.4'),
                'rural': Decimal('71.6')
            },
            'MR042': {  # Maghama
                'population': 89745,
                'male': Decimal('48.2'),
                'female': Decimal('51.8'),
                'urban': Decimal('24.2'),
                'rural': Decimal('75.8')
            },
            'MR043': {  # M'Bout
                'population': 98624,
                'male': Decimal('48.3'),
                'female': Decimal('51.7'),
                'urban': Decimal('25.1'),
                'rural': Decimal('74.9')
            },
            'MR044': {  # Monguel
                'population': 69797,
                'male': Decimal('48.4'),
                'female': Decimal('51.6'),
                'urban': Decimal('23.5'),
                'rural': Decimal('76.5')
            }
        }
    },
    'MR05': {  # Brakna
        'population': 374572,
        'male': Decimal('48.5'),
        'female': Decimal('51.5'),
        'urban': Decimal('27.2'),
        'rural': Decimal('72.8'),
        'departments': {
            'MR051': {  # Aleg
                'population': 108626,
                'male': Decimal('48.7'),
                'female': Decimal('51.3'),
                'urban': Decimal('29.4'),
                'rural': Decimal('70.6')
            },
            'MR052': {  # Bababé
                'population': 42183,
                'male': Decimal('48.3'),
                'female': Decimal('51.7'),
                'urban': Decimal('25.8'),
                'rural': Decimal('74.2')
            },
            'MR053': {  # Boghé
                'population': 95416,
                'male': Decimal('48.4'),
                'female': Decimal('51.6'),
                'urban': Decimal('27.6'),
                'rural': Decimal('72.4')
            },
            'MR054': {  # M'Bagne
                'population': 65550,
                'male': Decimal('48.5'),
                'female': Decimal('51.5'),
                'urban': Decimal('26.2'),
                'rural': Decimal('73.8')
            },
            'MR055': {  # Magta Lahjar
                'population': 62797,
                'male': Decimal('48.6'),
                'female': Decimal('51.4'),
                'urban': Decimal('25.4'),
                'rural': Decimal('74.6')
            }
        }
    },
    'MR06': {  # Trarza
        'population': 397589,
        'male': Decimal('48.7'),
        'female': Decimal('51.3'),
        'urban': Decimal('28.4'),
        'rural': Decimal('71.6'),
        'departments': {
            'MR061': {  # Boutilimit
                'population': 95421,
                'male': Decimal('48.8'),
                'female': Decimal('51.2'),
                'urban': Decimal('27.2'),
                'rural': Decimal('72.8')
            },
            'MR062': {  # Keur Macène
                'population': 42183,
                'male': Decimal('48.5'),
                'female': Decimal('51.5'),
                'urban': Decimal('26.8'),
                'rural': Decimal('73.2')
            },
            'MR063': {  # Mederdra
                'population': 52746,
                'male': Decimal('48.6'),
                'female': Decimal('51.4'),
                'urban': Decimal('27.4'),
                'rural': Decimal('72.6')
            },
            'MR064': {  # Ouad Naga
                'population': 48925,
                'male': Decimal('48.7'),
                'female': Decimal('51.3'),
                'urban': Decimal('26.5'),
                'rural': Decimal('73.5')
            },
            'MR065': {  # R'Kiz
                'population': 72614,
                'male': Decimal('48.8'),
                'female': Decimal('51.2'),
                'urban': Decimal('28.2'),
                'rural': Decimal('71.8')
            },
            'MR066': {  # Rosso
                'population': 85700,
                'male': Decimal('48.9'),
                'female': Decimal('51.1'),
                'urban': Decimal('31.5'),
                'rural': Decimal('68.5')
            }
        }
    },
    'MR07': {  # Adrar
        'population': 85635,
        'male': Decimal('49.2'),
        'female': Decimal('50.8'),
        'urban': Decimal('32.5'),
        'rural': Decimal('67.5'),
        'departments': {
            'MR071': {  # Aoujeft
                'population': 15426,
                'male': Decimal('49.1'),
                'female': Decimal('50.9'),
                'urban': Decimal('31.2'),
                'rural': Decimal('68.8')
            },
            'MR072': {  # Atar
                'population': 54283,
                'male': Decimal('49.3'),
                'female': Decimal('50.7'),
                'urban': Decimal('33.8'),
                'rural': Decimal('66.2')
            },
            'MR073': {  # Chinguetti
                'population': 15926,
                'male': Decimal('49.0'),
                'female': Decimal('51.0'),
                'urban': Decimal('30.8'),
                'rural': Decimal('69.2')
            }
        }
    },
    'MR08': {  # Dakhlet Nouadhibou
        'population': 162627,
        'male': Decimal('52.4'),
        'female': Decimal('47.6'),
        'urban': Decimal('87.5'),
        'rural': Decimal('12.5'),
        'departments': {
            'MR081': {  # Nouadhibou
                'population': 162627,
                'male': Decimal('52.4'),
                'female': Decimal('47.6'),
                'urban': Decimal('87.5'),
                'rural': Decimal('12.5')
            }
        }
    },
    'MR09': {  # Tagant
        'population': 95925,
        'male': Decimal('48.8'),
        'female': Decimal('51.2'),
        'urban': Decimal('29.5'),
        'rural': Decimal('70.5'),
        'departments': {
            'MR091': {  # Moudjeria
                'population': 28426,
                'male': Decimal('48.7'),
                'female': Decimal('51.3'),
                'urban': Decimal('28.2'),
                'rural': Decimal('71.8')
            },
            'MR092': {  # Tichit
                'population': 15283,
                'male': Decimal('48.6'),
                'female': Decimal('51.4'),
                'urban': Decimal('27.5'),
                'rural': Decimal('72.5')
            },
            'MR093': {  # Tidjikja
                'population': 52216,
                'male': Decimal('49.0'),
                'female': Decimal('51.0'),
                'urban': Decimal('31.2'),
                'rural': Decimal('68.8')
            }
        }
    },
    'MR10': {  # Guidimagha
        'population': 302196,
        'male': Decimal('48.5'),
        'female': Decimal('51.5'),
        'urban': Decimal('25.2'),
        'rural': Decimal('74.8'),
        'departments': {
            'MR101': {  # Ould Yengé
                'population': 125842,
                'male': Decimal('48.4'),
                'female': Decimal('51.6'),
                'urban': Decimal('26.5'),
                'rural': Decimal('73.5')
            },
            'MR102': {  # Sélibaby
                'population': 176354,
                'male': Decimal('48.6'),
                'female': Decimal('51.4'),
                'urban': Decimal('24.2'),
                'rural': Decimal('75.8')
            }
        }
    },
    'MR11': {  # Tiris Zemmour
        'population': 62829,
        'male': Decimal('51.8'),
        'female': Decimal('48.2'),
        'urban': Decimal('85.4'),
        'rural': Decimal('14.6'),
        'departments': {
            'MR111': {  # Bir Moghrein
                'population': 12584,
                'male': Decimal('51.5'),
                'female': Decimal('48.5'),
                'urban': Decimal('84.2'),
                'rural': Decimal('15.8')
            },
            'MR112': {  # F'Dérik
                'population': 8245,
                'male': Decimal('51.6'),
                'female': Decimal('48.4'),
                'urban': Decimal('83.8'),
                'rural': Decimal('16.2')
            },
            'MR113': {  # Zouérate
                'population': 42000,
                'male': Decimal('52.0'),
                'female': Decimal('48.0'),
                'urban': Decimal('86.5'),
                'rural': Decimal('13.5')
            }
        }
    },
    'MR12': {  # Inchiri
        'population': 28423,
        'male': Decimal('50.8'),
        'female': Decimal('49.2'),
        'urban': Decimal('82.5'),
        'rural': Decimal('17.5'),
        'departments': {
            'MR121': {  # Akjoujt
                'population': 28423,
                'male': Decimal('50.8'),
                'female': Decimal('49.2'),
                'urban': Decimal('82.5'),
                'rural': Decimal('17.5')
            }
        }
    },
    'MR13': {  # Nouakchott Ouest
        'population': 465152,
        'male': Decimal('50.2'),
        'female': Decimal('49.8'),
        'urban': Decimal('100.0'),
        'rural': Decimal('0.0'),
        'departments': {
            'MR131': {  # Ksar
                'population': 48521,
                'male': Decimal('50.1'),
                'female': Decimal('49.9'),
                'urban': Decimal('100.0'),
                'rural': Decimal('0.0')
            },
            'MR132': {  # Tevragh Zeina
                'population': 416631,
                'male': Decimal('50.3'),
                'female': Decimal('49.7'),
                'urban': Decimal('100.0'),
                'rural': Decimal('0.0')
            }
        }
    },
    'MR14': {  # Nouakchott Nord
        'population': 425142,
        'male': Decimal('50.4'),
        'female': Decimal('49.6'),
        'urban': Decimal('100.0'),
        'rural': Decimal('0.0'),
        'departments': {
            'MR141': {  # Dar Naim
                'population': 225418,
                'male': Decimal('50.5'),
                'female': Decimal('49.5'),
                'urban': Decimal('100.0'),
                'rural': Decimal('0.0')
            },
            'MR142': {  # Teyarett
                'population': 85124,
                'male': Decimal('50.2'),
                'female': Decimal('49.8'),
                'urban': Decimal('100.0'),
                'rural': Decimal('0.0')
            },
            'MR143': {  # Toujounine
                'population': 114600,
                'male': Decimal('50.4'),
                'female': Decimal('49.6'),
                'urban': Decimal('100.0'),
                'rural': Decimal('0.0')
            }
        }
    },
    'MR15': {  # Nouakchott Sud
        'population': 458467,
        'male': Decimal('50.3'),
        'female': Decimal('49.7'),
        'urban': Decimal('100.0'),
        'rural': Decimal('0.0'),
        'departments': {
            'MR151': {  # Arafat
                'population': 218426,
                'male': Decimal('50.4'),
                'female': Decimal('49.6'),
                'urban': Decimal('100.0'),
                'rural': Decimal('0.0')
            },
            'MR152': {  # El Mina
                'population': 185241,
                'male': Decimal('50.2'),
                'female': Decimal('49.8'),
                'urban': Decimal('100.0'),
                'rural': Decimal('0.0')
            },
            'MR153': {  # Riyadh
                'population': 54800,
                'male': Decimal('50.3'),
                'female': Decimal('49.7'),
                'urban': Decimal('100.0'),
                'rural': Decimal('0.0')
            }
        }
    }
}
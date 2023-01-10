# hydrus2d-gsa
notebooks for hydrus2d

## transect_reader.ipynb
* Source Data: 
  * `...\BHP Chile\2150 - BHP Chile - MEL Permeability Testing Program for SHL Ores\Hydrus model\
    * <sample name>\Raw data\`
      * e.g.  `Sulphide AND SCC\Raw data`
      
* Target Data: 
  * Criteria: 
 
    * Widths `w` - for depths `15, 30, 60?`
 
       * Dictionary:
 
         ```
           {'name' : 'Trnasects Across Section', 
           'keys' : 
              {'d' : {'depths' : [15, 30, 60] } ,
              'ss' : {'scheme' : [i for i in range(1,8)] } ,
              'c'  : {'cumulative irriation, cm' : [19.1, 38.2, 152.79, 1680.68] } ,
              'v'  : 'volumetric water content',
              'w'  : {'widths' : [0, 1.072435, 1.34055, 2.450817, 3.02774, 3.205063, 4.554471, 5.44732,
                                 5.870827, 6.354563, 7.117511, 7.733049, 8.244356, 9.532528, 9.804532, 
                                 10.39623, 11.26905, 11.80629, 12.5, 13.12224, 13.96607, 15.55549, 
                                 15.62715, 15.65822, 15.71829, 17.27864, 18.28292, 18.56758, 18.86337, 
                                 19.80064, 20.79559, 20.91391, 21.95756, 22.90886, 23.47451, 23.83693, 25]
                                  }
              }
            }
         ``` 
 
       * Logic: 
 
  ```
   for w in widths # new page
     for s in ss   # stack on same page
  ```
 
    | .   | .   | w   | w1  | w2  | w.. | wn  |
    | --- | --- | --- | --- | --- | --- | --- |
    | d1  | c1  | s   | v1  | v2  | v.. | vn  |  
    | d1  | c2  | s   | v1  | v2  | v.. | vn  |  
    | d1  | c3  | s   | v1  | v2  | v.. | vn  |  
    | d1  | c4  | s   | v1  | v2  | v.. | vn  |   
    | ... |     |     |     |     |     |     |   
 
 
    * Depths `d` - for widths `L (below emitter)` and `R (opposite emitter)`
 
      * Dictionary:
 
        ```
        {'name' : 'Profiles Below Emitter', 
        'keys' : 
          {'ts' : {'time emitter' : [" cm cum irr", " cm cum irr, mid off period", 
                                      " cm cum irr, before ON period"], 
           'ss' : {'scheme' : [i for i in range(1,8)] } ,
           'c'  : {'cumulative irriation, cm' : [19.1, 38.2, 152.79, 1680.68] } ,
           'v'  : 'volumetric water content',
           'd'  : {'depths' : [0, 1.666667, 3.333333, 5, 6.666667, 10, 13.33333, 18.33333, 25,
                               31.25, 37.5, 43.75, 50, 56.25, 62.5, 68.75, 75, 81.25, 87.5, 93.75, 
                               100, 106.25, 112.5, 118.75, 125, 131.25, 137.5, 143.75, 150, 
                               155.7143, 163.5714, 173.5714, 185.7143, 200]
                               }
           }
         }
         ``` 
 
      * Logic: 

  ` for t in ts `
 
    |    | s1  | s1  | s1  | s1  | |    | s2  | s2  | s2  | s2  | |
    | -- | --- | --- | --- | --- |-| -- | --- | --- | --- | --- |-|           
    |    | t   | t   | t   | t   | |    | t   | t   | t   | t   | |
    |    | s1  | s1  | s1  | s1  | |    | s2  | s2  | s2  | s2  | |
    |d   | c1  | c2  | c3  | c4  | |d   | c1  | c2  | c3  | c4  | |
    |0   | v   | v   | v   | v   | |0   | v   | v   | v   | v   | |
    |... | v   | v   | v   | v   | |... | v   | v   | v   | v   | |
    |200 | v   | v   | v   | v   | |200 | v   | v   | v   | v   | |
    |    |     |     |     |     | |    |     |     |     |     | |
    ...

 

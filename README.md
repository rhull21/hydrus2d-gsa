# hydrus2d-gsa
notebooks for hydrus2d

## transect_reader.ipynb
* Source Data: 
  * `...\BHP Chile\2150 - BHP Chile - MEL Permeability Testing Program for SHL Ores\Hydrus model\
    * <sample name>\Raw data\`
      * e.g.  `Sulphide AND SCC\Raw data`
      
* Target Data: 
  * Criteria: 
    * Widths - 16,30,60
        
 
    * Depths - L (below emitter), R (opposite emitter)
        ```
        {'name' : 'Profiles Below Emitter', 
        'keys' : 
          {'be' : {'below emitter' : [" cm cum irr", " cm cum irr, mid off period", 
                                      " cm cum irr, before ON period"], 
           's'  : {'scheme' : [i for i in range(1,8)] } ,
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

 | -- | --- | --- | --- | --- |-| -- | --- | --- | --- | --- | |           
 |    | be1 | be1 | be1 | be1 | |    | be1 | be1 | be1 | be1 | |
 |    | s1  | s1  | s1  | s1  | |    | s2  | s2  | s2  | s2  | |
 |d   | c1  | c2  | c3  | c4  | |d   | c1  | c2  | c3  | c4  | |
 |0   | v   | v   | v   | v   | |0   | v   | v   | v   | v   | |
 |.   | v   | v   | v   | v   | |.   | v   | v   | v   | v   | |
 |200 | v   | v   | v   | v   | |200 | v   | v   | v   | v   | |
 |    |     |     |     |     | |    |     |     |     |     | |
 |    | be2 | be2 | be2 | be2 | |    | be2 | be2 | be2 | be2 | |
 |    | s1  | s1  | s1  | s1  | |    | s2  | s2  | s2  | s2  | |
 |d   | c1  | c2  | c3  | c4  | |d   | c1  | c2  | c3  | c4  | |
 |0   | v   | v   | v   | v   | |0   | v   | v   | v   | v   | |
 |.   | v   | v   | v   | v   | |.   | v   | v   | v   | v   | |
 |200 | v   | v   | v   | v   | |200 | v   | v   | v   | v   | |

  

package src.pass1.structures.helper;

import src.pass1.structures.KPDT;
import src.pass1.structures.MDT;
import src.pass1.structures.PNT;

public class MNTRow {
        public String name;     // macro name
    public int pp;          // number of positional parameters
    public int kp;          // number of keyword parameters
    public int MDTP;        // macro definition table pointer
    public int KPDTP;       // keyword_parameter_default_table_pointer
    public int PNTP;        // parameter_name_table_pointer
    
    public MNTRow(String name, int pp, int kp){
        this.name = name;
        this.pp = pp;
        this.kp = kp;

        this.MDTP = MDT.getSize();
        if(pp != 0){ 
            this.PNTP = PNT.getSize();
        }
        else this.PNTP = -1;
        
        if(kp != 0){
            this.KPDTP = KPDT.getSize();
        }
        else this.KPDTP = -1;
    }

    @Override
    public String toString(){
        return this.name + " : " + this.pp + " : " + this.kp + " : " + this.MDTP + " : " + this.PNTP + " : " + this.KPDTP; 
    }

}

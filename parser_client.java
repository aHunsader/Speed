public class MyClass {
    public static void main(String args[]) {
        // Constants
        final int LEN_OF_STRING = 7; // should be LEN_OF_POS
        final int LEN_OF_ACC = 5;
        final int MAX_ACC = 80000;
        
        // RUN GPS Location here
        // We get these two values
        String user = "Allen";
        float lat = 37.7749f;
        float lon = -122.4194f;
        float acc_x = 214.12f;
        float acc_y = -57.3f;
        
        //PARSING CODE . . . 
        String output = user + "_";
        short sign;
        
        if (lat > 0) { sign = 0; } else { sign = 1; }
        int tmp = Math.round(lat*10000); // convert float to int * 100
        String numberAsString = String.valueOf(Math.abs(tmp));
        StringBuilder sb = new StringBuilder();
        while(sb.length()+numberAsString.length()<LEN_OF_STRING) {
            sb.append('0');
        }
        sb.append(Math.abs(tmp));
        if (sign == 1) { output = output + "-"; } else { output = output + "0"; }
        output = output + sb.toString() + "_";
        sb.setLength(0);
        
        if (lon > 0) { sign = 0; } else { sign = 1; }
        tmp = Math.round(lon*10000);
        numberAsString = String.valueOf(Math.abs(tmp));
        while(sb.length()+numberAsString.length()<LEN_OF_STRING) {
            sb.append('0');
        }
        sb.append(Math.abs(tmp));
        if (sign == 1) { output = output + "-"; } else { output = output + "0"; }
        output = output + sb.toString() + "_";
        sb.setLength(0);
        
        if (acc_x > 0) { sign = 0; } else { sign = 1; }
        tmp = Math.round(acc_x*100);
        numberAsString = String.valueOf(Math.abs(tmp));
        while(sb.length()+numberAsString.length()<LEN_OF_ACC) {
            sb.append('0');
        }
        sb.append(Math.abs(tmp));
        if (sign == 1) { output = output + "-"; } else { output = output + "0"; }
        output = output + sb.toString() + "_";
        sb.setLength(0);
        
        if (acc_y > 0) { sign = 0; } else { sign = 1; }
        tmp = Math.round(acc_y*100);
        numberAsString = String.valueOf(Math.abs(tmp));
        while(sb.length()+numberAsString.length()<LEN_OF_ACC) {
            sb.append('0');
        }
        sb.append(Math.abs(tmp));
        if (sign == 1) { output = output + "-"; } else { output = output + "0"; }
        output = output + sb.toString() + "_";
        
        output = output + "|_________";
        
        // RUN SOCKET Connection here : send output with updates lat and lon values every second
        System.out.println(output);
    }
}
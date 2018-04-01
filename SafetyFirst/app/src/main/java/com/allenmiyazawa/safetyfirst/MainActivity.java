package com.allenmiyazawa.safetyfirst;

import android.os.Bundle;
import android.os.Handler;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Timer;
import java.util.TimerTask;
import java.util.Random;

/**
 * Created by allenmiyazawa on 4/1/18.
 */

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    private TextView mTextViewReplyFromServer;
    private EditText mEditTextSendMessage;
    private GPSTracker tracker = new GPSTracker(this);

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button buttonSend = (Button) findViewById(R.id.btn_send);

        mEditTextSendMessage = (EditText) findViewById(R.id.edt_send_message);
        mTextViewReplyFromServer = (TextView) findViewById(R.id.tv_reply_from_server);

        buttonSend.setOnClickListener(this);

        if(!tracker.canGetLocation()){

            double latitude1= 34.071597;
            double longitude1 = -118.45003790000001;

            // \n is for new line
            Toast.makeText(getApplicationContext(), "Your Location is - \nLat: " + latitude1 + "\nLong: " + longitude1, Toast.LENGTH_LONG).show();
        }else{
            // can't get location
            // GPS or Network is not enabled
            // Ask user to enable GPS/network in settings
            tracker.showSettingsAlert();
        }
    }
    @Override
    public void onClick(View v) {

        switch (v.getId()) {

            case R.id.btn_send:
                // sendMessage(mEditTextSendMessage.getText().toString());
                sendMessage();
                break;
        }
    }



    private void sendMessage() {

        final Handler handler = new Handler();
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {

                try {
                    Socket socket = new Socket("164.67.2.6", 4136);
                    if (socket.isConnected()) {
                        PrintWriter out = new PrintWriter(
                                new BufferedWriter(
                                        new OutputStreamWriter(
                                                socket.getOutputStream())), true);
                        out.println("Latitude" + "Longitude");
                        out.close();
                        socket.close();
                    }
                } catch (UnknownHostException e) {
                    e.printStackTrace();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

//                try {
//                    //Replace below IP with the IP of that device in which server socket open.
//                    //If you change port then change the port number in the server side code also.
//                    Socket s = new Socket("164.67.2.6", 4136);
//
//                    OutputStream out = s.getOutputStream();
//
//                    final PrintWriter output = new PrintWriter(
//                            new BufferedWriter(
//                                    new OutputStreamWriter(
//                                            s.getOutputStream())), true);
//
//
//                    Timer timer = new Timer();
//                    timer.schedule(new TimerTask() {
//                        @Override
//                        public void run() {
//                            double lati = 34061597 + Math.random() * ((34081597 - 34061597) + 1);
//                            lati = lati/1000000;
//                            double longi = -118.45003790000001 + Math.random() * ((-118.45003780000001 + 1184.5003790000001) + 1);
//                            output.println(lati + "," + longi + "/");
//                            System.out.println("Data Sent");
//                        }
//                    }, 1000, 1000);
//
//                    //output.println(msg);
//
//                    output.flush();
//                    /*
//                    BufferedReader input = new BufferedReader(new InputStreamReader(s.getInputStream()));
//                    final String st = input.readLine();
//
//                    handler.post(new Runnable() {
//                        @Override
//                        public void run() {
//
//                            String s = mTextViewReplyFromServer.getText().toString();
//                            if (st.trim().length() != 0)
//                                mTextViewReplyFromServer.setText(s + "\nFrom Server : " + st);
//                        }
//                    });
//                    */
//                    output.close();
//                    out.close();
//                    s.close();
//                } catch (IOException e) {
//                    e.printStackTrace();
//                }
//            }
        });

        thread.start();
    }
}
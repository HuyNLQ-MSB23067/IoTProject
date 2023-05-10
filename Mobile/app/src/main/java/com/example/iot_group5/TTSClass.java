package com.example.iot_group5;

import android.content.Context;
import android.content.Intent;
import android.speech.tts.TextToSpeech;

import java.util.Locale;

public abstract class TTSClass extends Context implements TextToSpeech.OnInitListener {
    private int DATA_CHECKING = 0;
    private TextToSpeech niceTTS;
    @Override
    public void onInit(int initStatus) {
        if (initStatus == TextToSpeech.SUCCESS) {
            niceTTS.setLanguage(Locale.forLanguageTag("VI"));
            talkToMe("Xin chào các bạn, tôi là hệ thống nhận diện khuôn mặt");
        }
    }
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        //do they have the data
        if (requestCode == DATA_CHECKING) {
            //yep - go ahead and instantiate
            if (resultCode == TextToSpeech.Engine.CHECK_VOICE_DATA_PASS)
                niceTTS = new TextToSpeech(this, this);
                //no data, prompt to install it
            else {
                Intent promptInstall = new Intent();
                promptInstall.setAction(TextToSpeech.Engine.ACTION_INSTALL_TTS_DATA);
                startActivity(promptInstall);
            }
        }
    }

    public void talkToMe(String sentence) {
        String speakWords = sentence;
        niceTTS.speak(speakWords, TextToSpeech.QUEUE_FLUSH, null);
    }
}

package com.example.android.capstone.ceg

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.Menu
import android.view.MenuItem
import android.widget.Toast
import com.android.example.camerax.tflite.R
import com.google.android.material.appbar.AppBarLayout


class HomeActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)

        setSupportActionBar(findViewById(R.id.topAppBar))

    }

    override fun onCreateOptionsMenu(menu: Menu):Boolean{
        menuInflater.inflate(R.menu.top_app_bar,menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem) = when (item.itemId) {
        R.id.objectDetection -> {
            //Start Object Detection Activity
            val objectDetectorIntent =  Intent(this, CameraActivity::class.java)
            startActivity(objectDetectorIntent);
            finish();
            true
        }

        R.id.obstacleDetection -> {
            // User chose the "Favorite" action, mark the current item
            // as a favorite...
            true
        }

        else -> {
            // If we got here, the user's action was not recognized.
            // Invoke the superclass to handle it.
            super.onOptionsItemSelected(item)
        }
    }


}
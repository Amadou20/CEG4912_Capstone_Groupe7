package com.example.android.capstone.ceg

import android.content.Intent
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.drawerlayout.widget.DrawerLayout
import com.android.example.camerax.tflite.R
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.material.appbar.MaterialToolbar
import com.google.android.material.navigation.NavigationView
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase


class HomeActivity : AppCompatActivity() {
    private var topAppBar: MaterialToolbar? = null
    private var drawerLayout: DrawerLayout? = null
    private var navigationView:NavigationView?= null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_home)
         topAppBar = findViewById(R.id.topAppBar)
         setSupportActionBar(topAppBar)
         drawerLayout = findViewById(R.id.drawerLayout)

        topAppBar?.setNavigationOnClickListener {
            drawerLayout?.open()

        }

         navigationView = findViewById(R.id.navigation)
        navigationView?.setNavigationItemSelectedListener { menuItem ->
            // Handle menu item selected
            when(menuItem.itemId){
                R.id.objectDetection -> {
                    //Start Object Detection Activity
                    val objectDetectorIntent =  Intent(this, CameraActivity::class.java)
                    startActivity(objectDetectorIntent);
                    finish()
                    true
                }


                R.id.logOut -> {
                    GoogleSignIn.getClient(
                        this,
                        GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN).build()
                    ).signOut()

                    // firebase user
                    Firebase.auth.signOut()
                    // Go back to starting screen after logout
                    val SignInActivityIntent =  Intent(this, GoogleSignInActivity::class.java)
                    startActivity(SignInActivityIntent);
                    finish()
                    true
                }

                else -> {
                    // If we got here, the user's action was not recognized.
                    // Invoke the superclass to handle it.
                    super.onOptionsItemSelected(menuItem)
                }
            }
            menuItem.isChecked = true
            drawerLayout?.close()
            true
        }


    }






}
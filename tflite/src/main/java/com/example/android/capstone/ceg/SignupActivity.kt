package com.example.android.capstone.ceg

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.text.TextUtils
import android.util.Patterns
import android.view.View
import android.widget.Button
import android.widget.Toast
import com.android.example.camerax.tflite.R
import com.google.android.gms.tasks.OnCompleteListener
import com.google.android.material.textfield.TextInputLayout
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase
import models.ReadAndWrite
import models.User

class SignupActivity : AppCompatActivity() {

    private var firstnameLay:TextInputLayout? = null
    private var lastnameLay:TextInputLayout? = null
    private var emailLay:TextInputLayout? = null
    private var passwordLay:TextInputLayout? = null
    private var confirmPassLay:TextInputLayout? = null
    private var register: Button? = null

    private lateinit var auth: FirebaseAuth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_signup)

        firstnameLay = findViewById(R.id.firstname)
        lastnameLay = findViewById(R.id.lastname)
        emailLay= findViewById(R.id.email)
        passwordLay= findViewById(R.id.password)
        confirmPassLay = findViewById(R.id.confirmPass)
        register = findViewById(R.id.create)

        auth = Firebase.auth

        /*
            check if every field is successfully filled
            create a new User
            Save new user in the database
            start home Page
        */
        register?.setOnClickListener(object:View.OnClickListener {
            override fun onClick(view: View?) {
                // Do some work here
                val fname:String = firstnameLay?.editText?.text.toString()
                val lname:String = lastnameLay?.editText?.text.toString()
                val mail:String = emailLay?.editText?.text.toString()
                val pass:String = passwordLay?.editText?.text.toString()

                if(checkForm() == true){
                    val user = User(fname,lname,mail,pass)
                    auth.createUserWithEmailAndPassword(mail, pass) // create user for email password authentification
                    ReadAndWrite.initializeDbRef()
                    ReadAndWrite.writeNewUser(user)
                    val text = "Account successfully created!"
                    val duration = Toast.LENGTH_SHORT
                    val toast = Toast.makeText(applicationContext, text, duration)
                    toast.show()
                    updateUI()
                }
            }

        })

    }

    fun isEmail(text:TextInputLayout? ):Boolean {
        val email:CharSequence = text?.editText?.text.toString()
        return(!TextUtils.isEmpty(email) && Patterns.EMAIL_ADDRESS.matcher(email).matches())
    }

    fun isEmpty(text:TextInputLayout?):Boolean{
        val txt:CharSequence = text?.editText?.text.toString()
        return TextUtils.isEmpty(txt)
    }

    fun  checkForm():Boolean{
        var isValid: Boolean = true
        if(isEmpty(firstnameLay)){
            firstnameLay?.error ="firstname field empty"
            firstnameLay?.setErrorEnabled(true)
            isValid = false
        }

        if(isEmpty(lastnameLay)){
            lastnameLay?.error ="lastname field empty"
            lastnameLay?.setErrorEnabled(true)
            isValid = false
        }

        if(isEmpty(passwordLay) && passwordLay?.editText?.text.toString().equals( confirmPassLay?.editText?.text.toString() )){
            passwordLay?.error ="password field empty"
            passwordLay?.setErrorEnabled(true)
            isValid = false
        }

        if(isEmail(emailLay) == false){
            emailLay?.error ="please enter an correct email"
            emailLay?.setErrorEnabled(true)
            isValid = false
        }

        return isValid
    }

    fun updateUI(){
        var HomeActivityIntent= Intent(this,HomeActivity::class.java)
        startActivity(HomeActivityIntent)
        finish()
    }



}
package models

import com.google.firebase.database.DatabaseReference
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase


abstract class ReadAndWrite {
    private val TAG = "ReadAndWrite"

    //start write new objectDetected
    companion object{
        private lateinit var database: DatabaseReference
        private var m = mutableSetOf<String>()
        private var s = mutableMapOf<String,Int>()


        fun initializeDbRef(){
            database = Firebase.database.reference
        }

        fun writeNewObject(label:String,score:Float){
            val key: String? = database.child("object").getKey()
            val obj = ObjectDetected(label,score)

            if (key != null && !s.contains(label)) {
               database.child("object").child(label).setValue(obj)
               // m.add(label)
                s.set(label,1)

                //database.child("object").push().setValue(obj)
            } else{
                if (key != null) {
                    s.put(label,s.getOrPut(label){1}+1)
                    obj.count = s.getValue(label)

                    database.child("object").child(label).setValue(obj)
                }

            }
        }

        fun writeNewUser(user: User){
            val ref: DatabaseReference = database.child("Users").push()
            ref.setValue(user)
        }

    }




}
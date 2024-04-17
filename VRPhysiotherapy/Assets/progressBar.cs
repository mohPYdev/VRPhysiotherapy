using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class progressBar : MonoBehaviour
{
    public Slider slider;
    private float targetProgress=0;
    public float Fillspeed=0.5f;

    // Start is called before the first frame update
    void Start()
    {
      IncrementProgress(0.75f);  
    }

    // Update is called once per frame
    void Update()
    {
     if(slider.value < targetProgress)
        slider.value += Fillspeed * Time.deltaTime;   
    }
    public void IncrementProgress(float newProgress)
    {
       targetProgress= slider.value + newProgress;
    }
}

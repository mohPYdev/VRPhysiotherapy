using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class test : MonoBehaviour
{
    public GameObject intract;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    void OnTriggerEnter(Collider other)
    {
        intract.SetActive(true);
    }

    void OnTriggerStay(Collider other)
    {
       
    }

    void OnTriggerExit(Collider other)
    {
        intract.SetActive(false);
    }


    public void start_collision()
    {
        intract.SetActive(true);
    }

    public void stop_collision()
    {
        intract.SetActive(false);
    }
}

using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.XR.Interaction.Toolkit;
using UnityEngine.SceneManagement;
using TMPro;

public class RayHit : MonoBehaviour
{
    public XRController leftHandController;
    public XRController RighttHandController;

    
    public GameObject textObject;
    public GameObject menu;
    public void active_text()
    {
        if (! menu.activeSelf)
        {
            textObject.SetActive(true);
        }
    }
    public void deactive_text()
    {
        textObject.SetActive(false);
    }
    public void show_menu()
    {
        if (! menu.activeSelf)
        {         
            menu.SetActive(true);
            textObject.SetActive(false);
            Time.timeScale = 0.0f;
        }   
    }
    public void disappear_menu()
    {
        
        menu.SetActive(false);
        Time.timeScale = 1.0f;
    }
    public void go_main_menu()
    {
        SceneManager.LoadScene(0);
    }
    public void go_training()
    {
        SceneManager.LoadScene(1);
    }

}


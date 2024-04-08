using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
public class OptionPanelControl : MonoBehaviour
{
    public Slider music_level, sfx_level;
    public Button music_button, sfx_button;
    int music_count = 0,sfx_count=0;
    
    private void Start()
    {
        music_level.value = 1.0f;
        sfx_level.value = 1.0f;
    }
    
    public void Music_Mute()
    {
        music_count++;
        if (music_count%2 == 0)
        {
            change_transparency(music_button, 1.0f);
        }
        else
        {
            change_transparency(music_button, 0.3f);
        }
        AudioManager.instance.ToggleMusic();
    }

    public void SFX_Mute() 
    {
        sfx_count ++;
        if (sfx_count % 2 == 0)
        {
            change_transparency(sfx_button, 1.0f);
        }
        else
        {
            change_transparency(sfx_button, 0.3f);
        }
        AudioManager.instance.ToggleSFX();
    }

    void change_transparency(Button button,float transparency)
    {
        // Get the image component attached to the button
        Image buttonImage = button.GetComponent<Image>();

        // Ensure that the image component is not null
        if (buttonImage != null)
        {
            // Get the current color of the image
            Color currentColor = buttonImage.color;

            // Modify the alpha component of the color to adjust transparency
            currentColor.a = transparency;

            // Apply the modified color to the image
            buttonImage.color = currentColor;
        }
    }


    public void music_volume_change()
    {
        AudioManager.instance.MusicVolume(music_level.value);
    }
    public void sfx_volume_change()
    {
        AudioManager.instance.SFXVolume(sfx_level.value);
    }
}

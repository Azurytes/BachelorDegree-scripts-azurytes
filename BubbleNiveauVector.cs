using System.Collections;
using System.Collections.Generic;
using UnityEngine;

//[ExecuteInEditMode]
public class BubbleNiveauVector : MonoBehaviour
{
    Vector3 lastPos;
    Vector3 velocity;
    Vector3 lastRot;
    Vector3 angularVelocity;
    public Transform childBubbleMiddle;
    public Transform childBubbleRight;
    public Transform childBubbleLeft;
    Vector3 basePosBubbleMiddle;
    Vector3 basePosBubbleRight;
    Vector3 basePosBubbleLeft;
    Vector3 posBubbleMiddle;
    Vector3 posBubbleRight;
    Vector3 posBubbleLeft;
    public float maxWobble = 0.0003f;
    public float wobbleSpeed = 2f;
    public float recovery = 1f;
    float wobbleAmountX;
    float wobbleAmountZ;
    float wobbleAmountY;
    float wobbleAmountToAddX;
    float wobbleAmountToAddZ;
    float wobbleAmountToAddY;
    float pulse;
    float time = 0.5f;

    // Start is called before the first frame update
    void Start()
    {
        childBubbleMiddle = this.gameObject.transform.Find("bulle_middle");
        childBubbleRight = this.gameObject.transform.Find("bulle_right");
        childBubbleLeft = this.gameObject.transform.Find("bulle_left");
        basePosBubbleMiddle = childBubbleMiddle.transform.localPosition;
        basePosBubbleRight = childBubbleRight.transform.localPosition;
        basePosBubbleLeft = childBubbleLeft.transform.localPosition;
    }


    // Update is called once per frame
    void Update()
    {
        //middle bubble position change with tilt
        Vector3 bubbleDispMiddle = Vector3.Project(Vector3.up, childBubbleMiddle.transform.right);
        Vector3 bubbleDispYmiddle = Vector3.Project(Vector3.up, childBubbleMiddle.transform.up);
        Vector3 bubbleDispYmidLocal = transform.InverseTransformVector(bubbleDispYmiddle);
        Vector3 bubbleDispZmiddle = Vector3.Project(Vector3.up, childBubbleMiddle.transform.forward);
        Vector3 bubbleDispZmidLocal = transform.InverseTransformVector(bubbleDispZmiddle);
        posBubbleMiddle = (transform.InverseTransformVector(bubbleDispMiddle) * 0.01f) + basePosBubbleMiddle;
        posBubbleMiddle.y = (Unity.Mathematics.math.remap(-1, 1, -1, 0, (bubbleDispYmidLocal.y)) * 0.002f) + basePosBubbleMiddle.y;
        posBubbleMiddle.z = (bubbleDispZmidLocal.z * 0.001f) + basePosBubbleMiddle.z;
        //Debug.Log("new posBubbleMid: " + Unity.Mathematics.math.remap(-1, 1, -1, 0, (bubbleDispYmidLocal.y)));

        //right bubble position change with tilt
        Vector3 bubbleDispRight = Vector3.Project(Vector3.up, childBubbleRight.transform.right);
        Vector3 bubbleDispYright = Vector3.Project(Vector3.up, childBubbleRight.transform.up);
        Vector3 bubbleDispYrigthLocal = transform.InverseTransformVector(bubbleDispYright);
        Vector3 bubbleDispZright = Vector3.Project(Vector3.up, childBubbleRight.transform.forward);
        Vector3 bubbleDispZrigthLocal = transform.InverseTransformVector(bubbleDispZright);
        posBubbleRight = (transform.InverseTransformVector(bubbleDispRight) * 0.01f) + basePosBubbleRight;
        posBubbleRight.y = (Unity.Mathematics.math.remap(-1, 1, -1, 0, (bubbleDispYrigthLocal.y)) * 0.0015f) + basePosBubbleRight.y;
        posBubbleRight.z = (bubbleDispZrigthLocal.z * 0.0006f) + basePosBubbleRight.z;

        //left bubble position change with tilt
        Vector3 bubbleDispLeft = Vector3.Project(Vector3.up, childBubbleLeft.transform.up);
        Vector3 bubbleDispLeftLocal = transform.InverseTransformVector(bubbleDispLeft);
        Vector3 bubbleDispXleft = Vector3.Project(Vector3.up, childBubbleLeft.transform.right);
        Vector3 bubbleDispZleft = Vector3.Project(Vector3.up, childBubbleLeft.transform.forward);
        Vector3 bubbleDispZleftLocal = transform.InverseTransformVector(bubbleDispZleft);
        posBubbleLeft = (transform.InverseTransformVector(bubbleDispXleft) * 0.0005f) + basePosBubbleLeft;
        //Debug.Log("posBubbleLeft: " + bubbleDispLeftLocal.y);
        posBubbleLeft.y = (Unity.Mathematics.math.remap(-1, 1, -1, 0, (bubbleDispLeftLocal.y)) * 0.012f) + basePosBubbleLeft.y;
        //Debug.Log("new posBubbleLeft: " + bubbleDispLeftLocal.y);
        posBubbleLeft.z = (bubbleDispZleftLocal.z * 0.0005f) + basePosBubbleLeft.z;

        time += Time.deltaTime;
        // decrease wobble over time
        wobbleAmountToAddX = Mathf.Lerp(wobbleAmountToAddX, 0, Time.deltaTime * (recovery));
        wobbleAmountToAddZ = Mathf.Lerp(wobbleAmountToAddZ, 0, Time.deltaTime * (recovery));
        wobbleAmountToAddY = Mathf.Lerp(wobbleAmountToAddY, 0, Time.deltaTime * (recovery));

        // velocity
        velocity = (lastPos - transform.position) / Time.deltaTime;
        angularVelocity = transform.rotation.eulerAngles - lastRot;

        // make a sine wave of the decreasing wobble
        pulse = 2 * Mathf.PI * wobbleSpeed;
        wobbleAmountX = wobbleAmountToAddX * Mathf.Sin(pulse * time);
        wobbleAmountZ = wobbleAmountToAddZ * Mathf.Sin(pulse * time);
        wobbleAmountY = wobbleAmountToAddY * Mathf.Sin(pulse * time);

        // add clamped velocity to wobble
        wobbleAmountToAddX += Mathf.Clamp((velocity.x + (angularVelocity.z * 0.2f)) * maxWobble, -maxWobble, maxWobble);
        wobbleAmountToAddZ += Mathf.Clamp((velocity.z + (angularVelocity.x * 0.2f) + (angularVelocity.y * 0.2f)) * maxWobble, -maxWobble, maxWobble) * 0.2f;
        wobbleAmountToAddY += Mathf.Clamp(velocity.y * maxWobble, -maxWobble, maxWobble) * 0.75f;

        // keep last position
        lastPos = transform.position;
        lastRot = transform.rotation.eulerAngles;

        //transfer position value to bubbles
        posBubbleMiddle.x += wobbleAmountX;
        posBubbleMiddle.z += wobbleAmountZ;
        posBubbleMiddle.y += Mathf.Clamp(wobbleAmountY, -1, 0);
        //Debug.Log("float wobbleAmountY: " + Mathf.Clamp(wobbleAmountY, -1, 0));
        //Debug.Log("float wobbleAmountY: " + mapValues(-maxWobble, maxWobble, -maxWobble, 0, wobbleAmountY));
        //Debug.Log("float posBubbleMiddle.y: " + Unity.Mathematics.math.remap(-maxWobble, maxWobble, -maxWobble, 0f, wobbleAmountY));

        posBubbleRight.x += wobbleAmountX;
        posBubbleRight.z += wobbleAmountZ;
        posBubbleRight.y += Mathf.Clamp(wobbleAmountY, -1, 0);
        
        posBubbleLeft.x += wobbleAmountX * 0.1f;
        posBubbleLeft.z += wobbleAmountZ;
        posBubbleLeft.y += Mathf.Clamp(wobbleAmountY, -1, 0);

        childBubbleMiddle.transform.localPosition = posBubbleMiddle;
        childBubbleRight.transform.localPosition = posBubbleRight;
        childBubbleLeft.transform.localPosition = posBubbleLeft;
    }
}

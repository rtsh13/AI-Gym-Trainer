import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-info',
  templateUrl: './info.component.html',
  styleUrls: ['./info.component.css']
})
export class InfoComponent implements OnInit {

  form: FormGroup;
  equipmentList:string[]=['Barbell','Dumbell'];
  exerciseList:string[]=['Squats','Bicep curls','Side leg lift','Diamond pushups','Normal pushups','Jumping jacks','Lunges','Concentration Curls','Knee pushups','Chair squats','Stationary lunges'];
  cameraList:string[]=['External','Internal'];

  constructor(private fb:FormBuilder,private http:HttpClient,private router:Router,private route:ActivatedRoute) { }

  ngOnInit(): void {
    this.form = this.fb.group({
      firstName:[''],
      lastName:[''],
      sets:[''],
      reps:[''],
      equipment:[''],
      exercise:[''],
      // camera:['']
    });
  }

  onSubmit(){
    const data = this.form.value;
    console.log(data);
    this.form.reset();
    this.http.post('http://127.0.0.1:5000/sendData',data).subscribe(result=>{
      console.log(result);
    });
    if (data.exercise == 'Bicep curls'){
      window.location.href = "http://127.0.0.1:5000/biceps"  
    }
    if (data.exercise == 'Squats'){
      window.location.href = "http://127.0.0.1:5000/squats"  
    }  
    if (data.exercise == 'Side leg lift'){
      window.location.href = "http://127.0.0.1:5000/sideLegLifts"  
    }
    if (data.exercise == 'Diamond pushups'){
      window.location.href = "http://127.0.0.1:5000/diamondPushups"  
    }
    if (data.exercise == 'Normal pushups'){
      window.location.href = "http://127.0.0.1:5000/diamondPushups"  
    }
    if (data.exercise == 'Jumping jacks'){
      window.location.href = "http://127.0.0.1:5000/jumpingJacks"  
    }
    if (data.exercise == 'Lunges'){
      window.location.href = "http://127.0.0.1:5000/lunges"  
    }
    if (data.exercise == 'Concentration Curls'){
      window.location.href = "http://127.0.0.1:5000/cc"  
    }
    if (data.exercise == 'Knee pushups'){
      window.location.href = "http://127.0.0.1:5000/kneePushups"  
    }
    if (data.exercise == 'Chair squats'){
      window.location.href = "http://127.0.0.1:5000/chairSquat"  
    }
    if (data.exercise == 'Stationary lunges'){
      window.location.href = "http://127.0.0.1:5000/stationaryLunges"  
    }

  }

  onClose(){
    this.form.reset();
  }

}

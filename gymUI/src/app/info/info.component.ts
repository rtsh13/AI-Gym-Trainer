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
  exerciseList:string[]=['Squats','Bicep curls','Side leg lift','Diamond pushups','Normal pushups','Jumping jacks'];
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
      camera:['']
    });
  }

  onSubmit(){
    const data = this.form.value;
    console.log(data);
    this.form.reset();
    this.http.post('http://127.0.0.1:5000/sendData',data).subscribe(result=>{
      console.log(result);
    });
  }

  onClose(){
    this.form.reset();
  }

}

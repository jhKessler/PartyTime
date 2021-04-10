import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-progressbar',
  templateUrl: './progressbar.component.html',
  styleUrls: ['./progressbar.component.scss']
})
export class ProgressbarComponent implements OnInit {

  @Input()
  percent = 0;

  constructor() { }

  ngOnInit(): void {
  }

}

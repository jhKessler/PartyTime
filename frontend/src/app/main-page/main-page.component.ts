import {Component, OnInit} from '@angular/core';
import {StatsService} from "../stats.service";
import * as moment from 'moment'

import { ChartOptions, ChartType, ChartDataSets } from 'chart.js';
import { Label } from 'ng2-charts';

@Component({
  selector: 'app-main-page',
  templateUrl: './main-page.component.html',
  styleUrls: ['./main-page.component.scss']
})
export class MainPageComponent implements OnInit {

  /*public lineChartData: ChartDataSets[] = [
    { data: [65, 59, 80, 81, 56, 55, 40], label: 'Series A' },
  ];
  public lineChartLabels: Label[] = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
  public lineChartOptions: (ChartOptions & { annotation: any }) = {
    annotation: true,
    responsive: true,
    scales: {
      xAxes: [{
        gridLines: {display: false}
      }],
      yAxes: [{
        gridLines: {display: false}
      }]
    },
    legend: {
      display: false
    }
  };
  public lineChartColors: Color[] = [
    {
      borderColor: 'white',
      backgroundColor: 'transparent',
      borderWidth: 2,
      pointBorderColor: 'white',
    },
  ];
  public lineChartLegend = true;
  public lineChartType = 'line';
  public lineChartPlugins = [];*/


  public barChartOptions: ChartOptions = {
    responsive: true,
    scales: {
      xAxes: [{
        gridLines: {display: false},
        ticks: {
          fontColor: 'rgb(210,210,210)'
        }
      }],
      yAxes: [{
        gridLines: {display: false},
        ticks: {
          min: 0,
          fontColor: 'rgb(210,210,210)'
        }
      }]
    },
    legend: {
      display: false
    },
    defaultColor: 'red'
  };
  public barChartLabels: Label[] = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'];
  public barChartType: ChartType = 'bar';

  public barChartData: ChartDataSets[] = [
    { data: [65, 59, 80, 81, 56, 55, 40], backgroundColor: 'rgba(255,255,255,0.5)' }
  ];

  constructor(public statsService: StatsService) {
  }

  ngOnInit(): void {
  }

  daysLeft(date: Date){
    return moment(date).diff(moment(), 'days');
  }

}

import {Component, OnInit} from '@angular/core';
import {StatsService} from "../stats.service";

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

  constructor(public statsService: StatsService) {
  }

  ngOnInit(): void {

  }

}

import {BrowserModule, Title} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {StatsPageComponent} from './main-page/stats-page.component';
import {RouterModule} from '@angular/router';
import {MainPageComponent} from './stats-page/main-page.component';
import {ChartsModule} from 'ng2-charts';
import {HttpClientModule} from "@angular/common/http";
import { ProgressbarComponent } from './progressbar/progressbar.component';

@NgModule({
  declarations: [
    AppComponent,
    StatsPageComponent,
    MainPageComponent,
    ProgressbarComponent
  ],
  imports: [
    BrowserModule,
    ChartsModule,
    HttpClientModule,
    RouterModule.forRoot([
      {
        path: '',
        pathMatch: 'full',
        component: MainPageComponent
      },
      {
        path: 'stats',
        component: StatsPageComponent
      }
    ])
  ],
  providers: [Title],
  bootstrap: [AppComponent]
})
export class AppModule {
}

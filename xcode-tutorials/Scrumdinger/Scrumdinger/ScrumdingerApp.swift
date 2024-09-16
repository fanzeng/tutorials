//
//  ScrumdingerApp.swift
//  Scrumdinger
//
//  Created by Fan Zeng on 26/8/2024.
//

import SwiftUI

@main
struct ScrumdingerApp: App {
    var body: some Scene {
        WindowGroup {
            ScrumView(scrums: DailyScrum.sampleData)
        }
    }
}

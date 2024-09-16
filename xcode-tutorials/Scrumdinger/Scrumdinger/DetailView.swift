//
//  DetailView.swift
//  Scrumdinger
//
//  Created by Fan Zeng on 16/9/2024.
//

import SwiftUI

struct DetailView: View {
    let scrum: DailyScrum
    var body: some View {
        Text("hello World!")
    }
}

struct DetailView_Previews: PreviewProvider {
    static var previews: some View {
        NavigationStack {
            DetailView(scrum: DailyScrum.sampleData[0])
        }
    }
}

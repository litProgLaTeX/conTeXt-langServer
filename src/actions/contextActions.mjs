
export function registerActions(ScopeActions) {

  //function loadComponent(thisScope, theScope, theTokens, callArgs) {
    
    
    ScopeActions.addScopedAction(
      'keyword.control.structure.context',
      import.meta.url,
      { },
      async function(thisScope, theScope, theTokens, theLine, theDoc, trace) {
        if (trace) {
          console.log("----------------------------------------------------------")
          console.log("loadComponent")
          console.log(`thisScope: ${thisScope}`)
          console.log(` theScope: ${theScope}`)
          console.log(`theTokens: ${theTokens}`)
          console.log(`  theLine: ${theLine}`)
          console.log(`   theDoc: ${theDoc}`)
          console.log("----------------------------------------------------------")
        }
      }
  )

}
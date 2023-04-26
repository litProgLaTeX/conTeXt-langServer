
export function registerActions(ScopeActions) {

  function startText(disp, ctx, aMessage, callArgs) {
    console.log("----------------------------------------------------------")
    console.log("statText")
    console.log(aMessage)
    console.log("----------------------------------------------------------")
    ctx.append({
      'method'   : 'startText',
      'msg'      : aMessage,
      'kwargs'   : callArgs,
      'dispType' : 'silly'
    })
  }

  ScopeActions.addScopedAction(
    'meta.context.starttext',
    import.meta.url,
    { },
    startText
  )

}
import lxml.etree as etree

PSRP_TEMPLATE = """
<Obj RefId="0">
  <MS>
    <Obj N="PowerShell" RefId="1">
      <MS>
        <Obj N="Cmds" RefId="2">
          <TN RefId="0">
            <T>System.Collections.Generic.List`1[[System.Management.Automation.PSObject, System.Management.Automation, Version=3.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35]]</T>
            <T>System.Object</T>
          </TN>
          <LST>
            <Obj RefId="3">
              <MS>
                <S N="Cmd">Invoke-expression</S>
                <B N="IsScript">false</B>
                <Nil N="UseLocalScope" />
                <Obj N="MergeMyResult" RefId="4">
                  <TN RefId="1">
                    <T>System.Management.Automation.Runspaces.PipelineResultTypes</T>
                    <T>System.Enum</T>
                    <T>System.ValueType</T>
                    <T>System.Object</T>
                  </TN>
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergeToResult" RefId="5">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergePreviousResults" RefId="6">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergeError" RefId="7">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergeWarning" RefId="8">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergeVerbose" RefId="9">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergeDebug" RefId="10">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="Args" RefId="11">
                  <TNRef RefId="0" />
                  <LST>
                    <Obj RefId="12">
                      <MS>
                        <S N="N">-Command</S>
                        <Nil N="V" />
                      </MS>
                    </Obj>
                    <Obj RefId="13">
                      <MS>
                        <Nil N="N" />
                        <S N="V">COMMAND HERE</S>
                      </MS>
                    </Obj>
                  </LST>
                </Obj>
              </MS>
            </Obj>
            <Obj RefId="14">
              <MS>
                <S N="Cmd">Out-string</S>
                <B N="IsScript">false</B>
                <Nil N="UseLocalScope" />
                <Obj N="MergeMyResult" RefId="15">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergeToResult" RefId="16">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergePreviousResults" RefId="17">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergeError" RefId="18">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergeWarning" RefId="19">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergeVerbose" RefId="20">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="MergeDebug" RefId="21">
                  <TNRef RefId="1" />
                  <ToString>None</ToString>
                  <I32>0</I32>
                </Obj>
                <Obj N="Args" RefId="22">
                  <TNRef RefId="0" />
                  <LST>
                    <Obj RefId="22">
                      <MS>
                         <S N="N">-Stream</S>
                         <Nil N="V" />
                      </MS>
                    </Obj>
                  </LST>
                </Obj>
              </MS>
            </Obj>
          </LST>
        </Obj>
        <B N="IsNested">false</B>
        <Nil N="History" />
        <B N="RedirectShellErrorOutputPipe">true</B>
      </MS>
    </Obj>
    <B N="NoInput">true</B>
    <Obj N="ApartmentState" RefId="23">
      <TN RefId="2">
        <T>System.Threading.ApartmentState</T>
        <T>System.Enum</T>
        <T>System.ValueType</T>
        <T>System.Object</T>
      </TN>
      <ToString>Unknown</ToString>
      <I32>2</I32>
    </Obj>
    <Obj N="RemoteStreamOptions" RefId="24">
      <TN RefId="3">
        <T>System.Management.Automation.RemoteStreamOptions</T>
        <T>System.Enum</T>
        <T>System.ValueType</T>
        <T>System.Object</T>
      </TN>
      <ToString>0</ToString>
      <I32>0</I32>
    </Obj>
    <B N="AddToHistory">true</B>
    <Obj N="HostInfo" RefId="25">
      <MS>
        <B N="_isHostNull">true</B>
        <B N="_isHostUINull">true</B>
        <B N="_isHostRawUINull">true</B>
        <B N="_useRunspaceHost">true</B>
      </MS>
    </Obj>
    <B N="IsNested">false</B>
  </MS>
</Obj>
"""

TEMPLATE_NOD = etree.fromstring(PSRP_TEMPLATE)


def get_pipeline_xml(command):
    assert isinstance(command, str)
    command_nod = TEMPLATE_NOD.findall(".//*[@RefId='13']/MS/S")[0]
    command_nod.text = command
    return etree.tostring(TEMPLATE_NOD, encoding='utf-8').decode('utf-8') + '\r\n'

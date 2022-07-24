from pyteal import *
from algosdk import account, mnemonic

def approval_program():

    code = ScratchVar(TealType.bytes)

    on_creation = Seq([

        code.store(Concat(Bytes("Program"),Bytes("base64","ASABACI="))),
        App.globalPut(Bytes("LsigInStr"), code.load()),
        App.globalPut(Bytes("LsigAddress"), Sha512_256(code.load())),
        Return(Int(1))

    ])

    update_or_delete_application = Seq([
        Assert(Txn.sender() == Global.creator_address()),
        Return(Int(1))
    ])

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
        [Txn.on_completion() == OnComplete.UpdateApplication, update_or_delete_application],
        [Txn.on_completion() == OnComplete.DeleteApplication, update_or_delete_application],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(0))],
        [Txn.on_completion() == OnComplete.ClearState, Return(Int(0))],
    )

    return program

def clear_state_program():
    return Int(0) 

with open('nft_subscription_approval.teal', 'w') as f:
    compiled = compileTeal(approval_program(), Mode.Application, version=6)
    f.write(compiled)

with open('nft_subscription_clear_state.teal', 'w') as f:
    compiled = compileTeal(clear_state_program(), Mode.Application, version=6)
    f.write(compiled)

// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xbas99.psi.Xbas99Types.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xbas99.psi.*;

public class Xbas99StatementBothImpl extends ASTWrapperPsiElement implements Xbas99StatementBoth {

  public Xbas99StatementBothImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99Visitor visitor) {
    visitor.visitStatementBoth(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xbas99Visitor) accept((Xbas99Visitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xbas99BangComment getBangComment() {
    return findChildByClass(Xbas99BangComment.class);
  }

  @Override
  @Nullable
  public Xbas99SBreak getSBreak() {
    return findChildByClass(Xbas99SBreak.class);
  }

  @Override
  @Nullable
  public Xbas99SCall getSCall() {
    return findChildByClass(Xbas99SCall.class);
  }

  @Override
  @Nullable
  public Xbas99SClose getSClose() {
    return findChildByClass(Xbas99SClose.class);
  }

  @Override
  @Nullable
  public Xbas99SData getSData() {
    return findChildByClass(Xbas99SData.class);
  }

  @Override
  @Nullable
  public Xbas99SDef getSDef() {
    return findChildByClass(Xbas99SDef.class);
  }

  @Override
  @Nullable
  public Xbas99SDelete getSDelete() {
    return findChildByClass(Xbas99SDelete.class);
  }

  @Override
  @Nullable
  public Xbas99SDim getSDim() {
    return findChildByClass(Xbas99SDim.class);
  }

  @Override
  @Nullable
  public Xbas99SDisplay getSDisplay() {
    return findChildByClass(Xbas99SDisplay.class);
  }

  @Override
  @Nullable
  public Xbas99SEnd getSEnd() {
    return findChildByClass(Xbas99SEnd.class);
  }

  @Override
  @Nullable
  public Xbas99SFor getSFor() {
    return findChildByClass(Xbas99SFor.class);
  }

  @Override
  @Nullable
  public Xbas99SGo getSGo() {
    return findChildByClass(Xbas99SGo.class);
  }

  @Override
  @Nullable
  public Xbas99SIf getSIf() {
    return findChildByClass(Xbas99SIf.class);
  }

  @Override
  @Nullable
  public Xbas99SImage getSImage() {
    return findChildByClass(Xbas99SImage.class);
  }

  @Override
  @Nullable
  public Xbas99SInput getSInput() {
    return findChildByClass(Xbas99SInput.class);
  }

  @Override
  @Nullable
  public Xbas99SLet getSLet() {
    return findChildByClass(Xbas99SLet.class);
  }

  @Override
  @Nullable
  public Xbas99SNext getSNext() {
    return findChildByClass(Xbas99SNext.class);
  }

  @Override
  @Nullable
  public Xbas99SOnGo getSOnGo() {
    return findChildByClass(Xbas99SOnGo.class);
  }

  @Override
  @Nullable
  public Xbas99SOpen getSOpen() {
    return findChildByClass(Xbas99SOpen.class);
  }

  @Override
  @Nullable
  public Xbas99SOption getSOption() {
    return findChildByClass(Xbas99SOption.class);
  }

  @Override
  @Nullable
  public Xbas99SPrint getSPrint() {
    return findChildByClass(Xbas99SPrint.class);
  }

  @Override
  @Nullable
  public Xbas99SRandomize getSRandomize() {
    return findChildByClass(Xbas99SRandomize.class);
  }

  @Override
  @Nullable
  public Xbas99SRead getSRead() {
    return findChildByClass(Xbas99SRead.class);
  }

  @Override
  @Nullable
  public Xbas99SRem getSRem() {
    return findChildByClass(Xbas99SRem.class);
  }

  @Override
  @Nullable
  public Xbas99SRestore getSRestore() {
    return findChildByClass(Xbas99SRestore.class);
  }

  @Override
  @Nullable
  public Xbas99SReturn getSReturn() {
    return findChildByClass(Xbas99SReturn.class);
  }

  @Override
  @Nullable
  public Xbas99SStop getSStop() {
    return findChildByClass(Xbas99SStop.class);
  }

  @Override
  @Nullable
  public Xbas99STrace getSTrace() {
    return findChildByClass(Xbas99STrace.class);
  }

}

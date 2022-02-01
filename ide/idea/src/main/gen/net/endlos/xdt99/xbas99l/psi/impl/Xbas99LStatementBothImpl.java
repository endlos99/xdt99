// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xbas99l.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xbas99l.psi.Xbas99LTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xbas99l.psi.*;

public class Xbas99LStatementBothImpl extends ASTWrapperPsiElement implements Xbas99LStatementBoth {

  public Xbas99LStatementBothImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xbas99LVisitor visitor) {
    visitor.visitStatementBoth(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xbas99LVisitor) accept((Xbas99LVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @Nullable
  public Xbas99LBangComment getBangComment() {
    return findChildByClass(Xbas99LBangComment.class);
  }

  @Override
  @Nullable
  public Xbas99LSBreak getSBreak() {
    return findChildByClass(Xbas99LSBreak.class);
  }

  @Override
  @Nullable
  public Xbas99LSCall getSCall() {
    return findChildByClass(Xbas99LSCall.class);
  }

  @Override
  @Nullable
  public Xbas99LSClose getSClose() {
    return findChildByClass(Xbas99LSClose.class);
  }

  @Override
  @Nullable
  public Xbas99LSData getSData() {
    return findChildByClass(Xbas99LSData.class);
  }

  @Override
  @Nullable
  public Xbas99LSDef getSDef() {
    return findChildByClass(Xbas99LSDef.class);
  }

  @Override
  @Nullable
  public Xbas99LSDelete getSDelete() {
    return findChildByClass(Xbas99LSDelete.class);
  }

  @Override
  @Nullable
  public Xbas99LSDim getSDim() {
    return findChildByClass(Xbas99LSDim.class);
  }

  @Override
  @Nullable
  public Xbas99LSDisplay getSDisplay() {
    return findChildByClass(Xbas99LSDisplay.class);
  }

  @Override
  @Nullable
  public Xbas99LSEnd getSEnd() {
    return findChildByClass(Xbas99LSEnd.class);
  }

  @Override
  @Nullable
  public Xbas99LSFor getSFor() {
    return findChildByClass(Xbas99LSFor.class);
  }

  @Override
  @Nullable
  public Xbas99LSGo getSGo() {
    return findChildByClass(Xbas99LSGo.class);
  }

  @Override
  @Nullable
  public Xbas99LSIf getSIf() {
    return findChildByClass(Xbas99LSIf.class);
  }

  @Override
  @Nullable
  public Xbas99LSImage getSImage() {
    return findChildByClass(Xbas99LSImage.class);
  }

  @Override
  @Nullable
  public Xbas99LSInput getSInput() {
    return findChildByClass(Xbas99LSInput.class);
  }

  @Override
  @Nullable
  public Xbas99LSLet getSLet() {
    return findChildByClass(Xbas99LSLet.class);
  }

  @Override
  @Nullable
  public Xbas99LSNext getSNext() {
    return findChildByClass(Xbas99LSNext.class);
  }

  @Override
  @Nullable
  public Xbas99LSOnGo getSOnGo() {
    return findChildByClass(Xbas99LSOnGo.class);
  }

  @Override
  @Nullable
  public Xbas99LSOpen getSOpen() {
    return findChildByClass(Xbas99LSOpen.class);
  }

  @Override
  @Nullable
  public Xbas99LSOption getSOption() {
    return findChildByClass(Xbas99LSOption.class);
  }

  @Override
  @Nullable
  public Xbas99LSPrint getSPrint() {
    return findChildByClass(Xbas99LSPrint.class);
  }

  @Override
  @Nullable
  public Xbas99LSRandomize getSRandomize() {
    return findChildByClass(Xbas99LSRandomize.class);
  }

  @Override
  @Nullable
  public Xbas99LSRead getSRead() {
    return findChildByClass(Xbas99LSRead.class);
  }

  @Override
  @Nullable
  public Xbas99LSRem getSRem() {
    return findChildByClass(Xbas99LSRem.class);
  }

  @Override
  @Nullable
  public Xbas99LSRestore getSRestore() {
    return findChildByClass(Xbas99LSRestore.class);
  }

  @Override
  @Nullable
  public Xbas99LSReturn getSReturn() {
    return findChildByClass(Xbas99LSReturn.class);
  }

  @Override
  @Nullable
  public Xbas99LSStop getSStop() {
    return findChildByClass(Xbas99LSStop.class);
  }

  @Override
  @Nullable
  public Xbas99LSTrace getSTrace() {
    return findChildByClass(Xbas99LSTrace.class);
  }

}

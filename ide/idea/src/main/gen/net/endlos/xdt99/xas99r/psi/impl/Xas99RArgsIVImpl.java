// This is a generated file. Not intended for manual editing.
package net.endlos.xdt99.xas99r.psi.impl;

import java.util.List;
import org.jetbrains.annotations.*;
import com.intellij.lang.ASTNode;
import com.intellij.psi.PsiElement;
import com.intellij.psi.PsiElementVisitor;
import com.intellij.psi.util.PsiTreeUtil;
import static net.endlos.xdt99.xas99r.psi.Xas99RTypes.*;
import com.intellij.extapi.psi.ASTWrapperPsiElement;
import net.endlos.xdt99.xas99r.psi.*;

public class Xas99RArgsIVImpl extends ASTWrapperPsiElement implements Xas99RArgsIV {

  public Xas99RArgsIVImpl(@NotNull ASTNode node) {
    super(node);
  }

  public void accept(@NotNull Xas99RVisitor visitor) {
    visitor.visitArgsIV(this);
  }

  @Override
  public void accept(@NotNull PsiElementVisitor visitor) {
    if (visitor instanceof Xas99RVisitor) accept((Xas99RVisitor)visitor);
    else super.accept(visitor);
  }

  @Override
  @NotNull
  public List<Xas99ROpLabel> getOpLabelList() {
    return PsiTreeUtil.getChildrenOfTypeAsList(this, Xas99ROpLabel.class);
  }

  @Override
  @Nullable
  public Xas99ROpRegister getOpRegister() {
    return findChildByClass(Xas99ROpRegister.class);
  }

}